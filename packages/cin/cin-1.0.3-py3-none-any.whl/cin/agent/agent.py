# Standard libraries
from datetime import datetime, timezone
import json
import os
from typing import Any, Callable
import uuid
from pydantic import BaseModel, Field, PrivateAttr, model_validator
import httpx
from logging import Logger

# Internal library
from ..tools import extract_tool_info, execution_completed
from ..utils import extract_json
from ..exceptions import ToolError, AgentError



class ActionResult(BaseModel):
    name: str
    description: str
    parameters: dict
    result: Any = Field(default=None, description="The result of the action execution")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"{self.name}: {self.description}\nParameters: {self.parameters}\nResult: {self.result}\nExecuted at: {self.created_at}"

    def get_formatted_result(self):
        return f"Action '{self.name}' was ran at {self.created_at} with parameters {self.parameters} and returned the following result:\n{self.result}"


class Session(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    entity_id: str = Field(..., description="The ID of the entity")
    actions: list[ActionResult] = Field(default_factory=list, description="A list of actions taken by the agent during the session")
    issues: list[str] = Field(default_factory=list, description="Any issues that occurred during execution, this could include parsing issues")


class Agent(BaseModel):
    name: str = Field(..., description="The name of the agent")
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    description: str = Field(default="You are a helpful assistant.", description="A brief description of the agent")
    endpoint: str = Field(default=None, description="The endpoint of the model provider")
    endpoint_connect_timeout: float = Field(default=10.0, description="The connect timeout for the endpoint")
    endpoint_read_timeout: float = Field(default=120.0, description="The read timeout for the endpoint")
    endpoint_write_timeout: float = Field(default=30.0, description="The write timeout for the endpoint")
    endpoint_pool_timeout: float = Field(default=30.0, description="The pool timeout for the endpoint")
    endpoint_retry_limit: int = Field(default=3, description="The retry limit for the endpoint")
    endpoint_retry_exponential_backoff_multiplier: float = Field(default=1.0, description="The retry exponential backoff multiplier for the endpoint")
    api_key : str = Field(default=None, description="The API key of the model provider")
    model: str = Field(default=None, description="The name of the model")
    instructions: str = Field(default="You are a helpful assistant.", description="Instructions for the agent")
    dos: list[str] = Field(default_factory=list, description="A list of things you want the agent to do")
    donots: list[str] = Field(default_factory=list, description="A list of things you do not want the agent to do")
    temperature: float = Field(default=0.5, description="The temperature of the model")
    top_p: float = Field(default=1.0, description="The top p value of the model")
    tool_agent_guidelines: str = Field(default="default", description="Guidelines for the agent on how to use resources (tools/agents)")
    tools: list[Callable] = Field(default_factory=list, description="A list of tools available to the agent in the form of callable functions")
    examples: str = Field(default=None, description="Examples of how to use the agent (will be appened to the end of the prompt)")
    interaction: list['Agent'] = Field(default_factory=list, description="A list of agents that the agent can interact with")
    refresh_actions_after_execution: bool = Field(default=True, description="Whether to refresh the agent's actions and issues taken after each execution, defaults to True to ensure Agent knows what it has done for the particular request")
    refresh_issues_after_execution: bool = Field(default=False, description="Whether to refresh the agent's issues taken after each execution, defaults to False to ensure agent can continuously learn from it's mistakes")
    logger: Logger = Field(default=None, description="A logger for the agent")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    # Runtime udpates
    _client: httpx.Client = PrivateAttr()
    _sessions: list[Session] = PrivateAttr(default_factory=list)
    _current_session: Session = PrivateAttr(default=None)

    class Config:
        arbitrary_types_allowed = True

    @model_validator(mode='after')
    def check_endpoints_models_and_apikeys(self):
        if self.endpoint == "openai-v1-chat-completions" and (
            self.model == "gpt-4o-2024-08-06" or
            self.model == "o1-mini-2024-09-12" or
            self.model == "gpt-4o-mini-2024-07-18"
            ):
            if self.api_key is None:
                self.api_key = os.getenv("OPENAI_API_KEY")
            if self.api_key is None:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            return self

        if self.endpoint == "anthropic-v1-messages" and self.model == "claude-3-5-sonnet-20241022":
            if self.api_key is None:
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if self.api_key is None:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
            return self

        raise ValueError(f"An endpoint '{self.endpoint}' and model name '{self.model}' is not supported. Please check the endpoint and model name.")

    @model_validator(mode='after')
    def check_tools(self):
        for tool in self.tools:
            if not callable(tool):
                raise ValueError(f"Tool '{tool}' is not callable.")

            if tool.__name__ in dir(self):
                raise ValueError(f"Tool '{tool.__name__}' is a reserved method name.")

        return self

    @model_validator(mode='after')
    def set_client(self):
        if self.endpoint:
            timeout = httpx.Timeout(
                connect=self.endpoint_connect_timeout,
                read=self.endpoint_read_timeout,
                write=self.endpoint_write_timeout,
                pool=self.endpoint_pool_timeout,
            )
            self._client = httpx.Client(timeout=timeout, transport=httpx.HTTPTransport(retries=self.endpoint_retry_limit))


        return self

    def model_post_init(self, __context: any) -> None:
        # Add the default tools to the agent
        self.tools.append(execution_completed)

    def log(self, level: str, message: str) -> None:
        if self.logger:
            if level == "debug":
                self.logger.debug(message)
                return
            if level == "info":
                self.logger.info(message)
                return
            elif level == "warning":
                self.logger.warning(message)
                return
            elif level == "error":
                self.logger.error(message)
                return
            elif level == "critical":
                self.logger.critical(message)
                return
        raise ValueError(f"Invalid log level '{level}'. Valid log levels are 'debug', 'info', 'warning', 'error', and 'critical'.")


    def _execute(self, input: str, instructions: str = None) -> str:
        # OpenAI - gpt-4o-mini-2024-07-18
        # https://platform.openai.com/docs/models#gpt-4o-mini - https://api.openai.com/v1/chat/completions
        if self.endpoint == "openai-v1-chat-completions" and self.model == "gpt-4o-mini-2024-07-18":
            url = "https://api.openai.com/v1/chat/completions"
            context_window = 128000
            max_output_tokens = 16384
            input_token_price_per_million_usd = 0.150
            output_token_price_per_million_usd = 0.600

            # If instructions are not provided, use the agent's execution instructions
            if instructions is None:
                input = self._format_input_for_execution(input=input)
                instructions = self._create_system_prompt()

            # Dynamically construct the headers
            headers = {}
            headers["Content-Type"] = "application/json"
            if self.api_key is not None:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Dynamically construct the payload
            payload = {}
            payload["model"] = self.model
            payload["messages"] = []
            if instructions is not None:
                payload["messages"].append({"role": "system", "content": instructions})
            if input is not None:
                payload["messages"].append({"role": "user", "content": input})
            if self.temperature is not None:
                payload["temperature"] = self.temperature
            if self.top_p is not None:
                payload["top_p"] = self.top_p

            # Send the request using httpx
            response = self._client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            return response_json['choices'][0]['message']['content']


        # OpenAI - GPT-4o-2024-08-06
        # https://platform.openai.com/docs/models#gpt-4o - https://api.openai.com/v1/chat/completions
        if self.endpoint == "openai-v1-chat-completions" and self.model == "gpt-4o-2024-08-06":
            url = "https://api.openai.com/v1/chat/completions"
            context_window = 128000
            max_output_tokens = 16384
            input_token_price_per_million_usd = 2.50
            output_token_price_per_million_usd = 10.00

            # If instructions are not provided, use the agent's execution instructions
            if instructions is None:
                input = self._format_input_for_execution(input=input)
                instructions = self._create_system_prompt()

            # Dynamically construct the headers
            headers = {}
            headers["Content-Type"] = "application/json"
            if self.api_key is not None:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Dynamically construct the payload
            payload = {}
            payload["model"] = self.model
            payload["messages"] = []
            if instructions is not None:
                payload["messages"].append({"role": "system", "content": instructions})
            if input is not None:
                payload["messages"].append({"role": "user", "content": input})
            if self.temperature is not None:
                payload["temperature"] = self.temperature
            if self.top_p is not None:
                payload["top_p"] = self.top_p

            # Send the request using httpx
            response = self._client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            return response_json['choices'][0]['message']['content']

        # OpenAI - o1-mini-2024-09-12
        # https://platform.openai.com/docs/guides/reasoning - https://platform.openai.com/docs/models#o1 - https://api.openai.com/v1/chat/completions
        if self.endpoint == "openai-v1-chat-completions" and self.model == "o1-mini-2024-09-12":
            url = "https://api.openai.com/v1/chat/completions"
            context_window = 128000
            max_output_tokens = 65536
            input_token_price_per_million_usd = 3.00
            output_token_price_per_million_usd = 12.00

            # If instructions are not provided, use the agent's execution instructions
            if instructions is None:
                input = self._format_input_for_execution(input=input)
                instructions = self._create_system_prompt()

            # o1-mini-2024-09-12 does not support system message, so we must concatenate the instructions with the input and only send the input
            if instructions is not None:
                input = instructions + "\n\n" + input

            # Dynamically construct the headers
            headers = {}
            headers["Content-Type"] = "application/json"
            if self.api_key is not None:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Dynamically construct the payload
            payload = {}
            payload["model"] = self.model
            payload["messages"] = []
            if input is not None:
                payload["messages"].append({"role": "user", "content": input})

            # Send the request using httpx
            response = self._client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            return response_json['choices'][0]['message']['content']

        # Anthropic - claude-3-5-sonnet-20241022
        # https://docs.anthropic.com/en/docs/about-claude/models - https://api.anthropic.com/v1/messages
        if self.endpoint == "anthropic-v1-messages" and self.model == "claude-3-5-sonnet-20241022":
            url = "https://api.anthropic.com/v1/messages"
            context_window = 200000
            max_output_tokens = 8192
            input_token_price_per_million_usd = 3.00
            output_token_price_per_million_usd = 15.00

            # If instructions are not provided, use the agent's execution instructions
            if instructions is None:
                input = self._format_input_for_execution(input=input)
                instructions = self._create_system_prompt()

            # Dynamically construct the headers
            headers = {}
            headers["Content-Type"] = "application/json"
            if self.api_key is not None:
                headers["x-api-key"] = self.api_key
            headers["anthropic-version"] = "2023-06-01"

            # Dynamically construct the payload
            payload = {}
            payload["model"] = self.model
            if instructions is not None:
                payload["system"] = instructions
            if max_output_tokens is not None:
                payload["max_tokens"] = max_output_tokens
            if input is not None:
                payload["messages"] = [{"role": "user", "content": input}]
            if self.temperature is not None:
                payload["temperature"] = self.temperature
            if self.top_p is not None:
                payload["top_p"] = self.top_p

            # Send the request using httpx
            response = self._client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            return response_json['content'][0]['text']

        raise Exception(f"An endpoint '{self.endpoint}' and model name '{self.model}' cannot execute the request. Please check the endpoint and model name.")

    def get_tool_information(self) -> str:
        if not self.tools:
            return None
        function_information = extract_tool_info(self.tools)
        return function_information

    def get_available_agents(self) -> str:
        if not self.interaction:
            return None
        agent_interaction_list = []
        for agent in self.interaction:
            agent_info = {
                "name": agent.name,
                "description": agent.description + " " + "Parameters: request (str): The information you are requesting from this agent. The request should start with I am requesting.. \n Returns: response",
            }

            # Convert the dictionary to a JSON-formatted string
            json_output = json.dumps(agent_info, indent=4)
            agent_interaction_list.append(json_output)

        # Join all JSON outputs with double newlines for better readability
        return "\n\n".join(agent_interaction_list)

    def _get_full_summary(self, input: str) -> str:
        # Create a summary of the agent's actions and issues
        summary_list = []

        # Append the user input
        summary_list.append(f"### User Input\n{input}")

        # Add the actions taken by the agent
        if self._current_session.actions:
            actions_information = "\n".join([tool_result.get_formatted_result() for tool_result in self._current_session.actions])
            summary_list.append(f"### I took these actions and received these results\n{actions_information}")

        # Check if self.actions is empty
        if not self._current_session.actions:
            summary_list.append("### I did not take any actions. Either I was unable to complete it due to issues or I did not have the tools to do so.")

        # Join all sections with double newlines for better readability
        summary = "\n\n".join(summary_list)

        # Create system prompt
        system_prompt = f"### Below is infomation that describes you\n{self.description}"
        system_prompt += "\n\n You will be provied a input from a user as well as a summary of all the actions you have taken and the results of those actions to the input. Your task is to provide an indepth response given all this information to the best of your ability."

        response = self._execute(input=summary, instructions=system_prompt)
        return response

    def _get_action_summary(self, input: str, reasoning: str) -> str:
        # Create a summary of the agent's actions and issues
        summary_list = []

        # Add the actions taken by the agent
        if self._current_session.actions:
            actions_information = "\n".join([tool_result.get_formatted_result() for tool_result in self._current_session.actions])
            summary_list.append(f"\n{actions_information}")

        # Check if self.actions is empty
        if not self._current_session.actions:
            summary_list.append(f"This agent did not take any actions. Either the agent was unable to complete it due to issues or it did not have the tools to do so. The reasoning for this is: {reasoning}")

        # Join all sections with double newlines for better readability
        return "\n\n".join(summary_list)

    def _format_input_for_execution(self, input: str) -> str:
        formatted_input = []
        formatted_input.append("### User Input\n<user_input>")
        formatted_input.append(input)
        formatted_input.append("</user_input>")
        formatted_input = "\n".join(formatted_input)
        return formatted_input

    def _update_current_session(self, entity_id: str) -> None:
        # If the current session is already set, clear it
        self._current_session = None

        # If entity_id is not provided, it is most likely a human, so let's create a new session for them
        if entity_id == None:
            self.log("info", f"Creating a new entity id for this entity because none was provided.")
            entity_id = uuid.uuid4().hex

        # Search for an existing session with the given entity_id
        for session in self._sessions:
            if session.entity_id == entity_id:
                self.log("info", f"Found an existing session with entity id '{entity_id}' we will use the past actions we have taken and issues.")
                self._current_session = session
                break

        # If no session is found, create a new session
        if not self._current_session:
            self.log("info", f"Creating a new session with entity id '{entity_id}' because we could not find an existing session")
            self._current_session = Session(
                entity_id=entity_id,
                actions=[])
            self._sessions.append(self._current_session)

        # If the session is not found or created, raise an error
        if self._current_session == None:
            raise ValueError(f"Session with entity_id '{entity_id}' not found or created.")


    def _create_system_prompt(self) -> str:
        system_prompt_with_interactions_and_tools_list = []

        # Add primary instructions here
        if self.instructions:
            instructions = []
            instructions.append("### Instructions\n<instructions>")
            instructions.append(self.instructions)
            instructions.append("</instructions>")
            instructions = "\n".join(instructions)
            system_prompt_with_interactions_and_tools_list.append(instructions)

        # Ensure the agent reflects the previous actions taken
        if self._current_session.actions:
            previous_actions = []
            previous_actions.append("### Previous Actions\nThese are the actions you have already taken, please review these before making a decision.\n<previous_actions>")
            previous_actions.extend(tool_result.get_formatted_result() for tool_result in self._current_session.actions)
            previous_actions.append("</previous_actions>")
            previous_actions = "\n".join(previous_actions)
            system_prompt_with_interactions_and_tools_list.append(previous_actions)
        else:
            previous_actions = []
            previous_actions.append("### Previous Actions\nThese are the actions you have already taken, please review these before making a decision.\n<previous_actions>")
            previous_actions.append("You have not taken any actions yet.")
            previous_actions.append("</previous_actions>")
            previous_actions = "\n".join(previous_actions)
            system_prompt_with_interactions_and_tools_list.append(previous_actions)

        # Add things you want the agent to do here
        if self.dos:
            dos = []
            dos.append("!VERY IMPORTANT These are the things you MUST do\n<things_you_must_do>")
            dos.extend(f"- {item}" for item in self.dos)
            dos.append("</things_you_must_do>")
            system_prompt_with_interactions_and_tools_list.append("\n".join(dos))

        # Add things you do not want the agent to do here
        if self.donots:
            donots = []
            donots.append("!VERY IMPORTANT These are the things you MUST NOT do\n<things_you_must_not_do>")
            donots.extend(f"- {item}" for item in self.donots)
            donots.append("</things_you_must_not_do>")
            system_prompt_with_interactions_and_tools_list.append("\n".join(donots))

        # Add tool information here
        if self.tools:
            tool_information = []
            tool_information.append("### Here are your available tools you can interact with:\n<available_tools>")
            tool_information.append(extract_tool_info(self.tools))
            tool_information.append("</available_tools>")
            tool_information = "\n".join(tool_information)
            system_prompt_with_interactions_and_tools_list.append(tool_information)

        # Add agent interaction information here
        if self.interaction:
            interactions = []
            interactions.append("### Below are your available agents you can interact with:\n<available_agents>")
            interactions.append(self.get_available_agents())
            interactions.append("</available_agents>")
            interactions = "\n".join(interactions)
            system_prompt_with_interactions_and_tools_list.append(interactions)

        # If no parameters are provided, use the default guidelines
        if self.tool_agent_guidelines == "default":
            tool_agent_guidelines = []
            tool_agent_guidelines.append("### Tool & Resource Guidelines\n<tool_agent_guidelines>")
            tool_agent_guidelines.append("1. **Sequential Usage:** When multiple tools or agents are needed to fulfill a request, they will be executed in the order they appear in the list, starting from the first item to the last.")
            tool_agent_guidelines.append("2. **Use Valid Parameters Only:** All parameters provided to tools or agents must be actual, valid values. Avoid using outputs from other tools or agents as parameters.")
            tool_agent_guidelines.append("3. **Handle Dependent Parameters Separately:** If a tool or agent's parameters depend on the output of a previous tool or agent, do not include them in the initial list. Dependencies will be managed separately.")
            tool_agent_guidelines.append("4. **Efficient Resource Utilization:** You are encouraged to use multiple resources if it enhances the response and improves efficiency by reducing the number of calls. Ensure each tool is used appropriately without relying on placeholder values.")
            tool_agent_guidelines.append("5. **Prioritize Tool/Agent Usage Over Personal Knowledge:** If information can be acquired through tools or agents, prioritize using them instead of relying solely on your own knowledge.")
            tool_agent_guidelines.append("6. **Exclusive Use of `execution_completed`:** When signaling the end of execution with the `execution_completed` tool, it **must be the only** tool or agent included in your response. **Do not** include any other tools, agents, or resources alongside `execution_completed`.")
            tool_agent_guidelines.append("7. **Reflect on Previous Actions Before Using a Tool:** Before deciding to use a tool or agent, review the actions you have already taken to address the request. This ensures efficiency, avoids redundancy, and leverages previous work effectively.")
            tool_agent_guidelines.append("</tool_agent_guidelines>")
            tool_agent_guidelines = "\n".join(tool_agent_guidelines)
            system_prompt_with_interactions_and_tools_list.append(tool_agent_guidelines)
        # If the user provides custom guidelines, use them
        elif self.tool_agent_guidelines not in ["default", None]:
            tool_agent_guidelines = []
            tool_agent_guidelines.append("### Tool & Resource Guidelines\n<tool_agent_guidelines>")
            tool_agent_guidelines.append(self.tool_agent_guidelines)
            tool_agent_guidelines.append("</tool_agent_guidelines>")
            tool_agent_guidelines = "\n".join(tool_agent_guidelines)
            system_prompt_with_interactions_and_tools_list.append(tool_agent_guidelines)
        # If user applies None to the guidelines, do not include them
        else:
            pass

        # If there have been any issues in past responses, add them here
        if self._current_session.issues:
            issues = []
            issues.append("### Previous Issues\nPlease **DO NOT RESPOND** in the following ways. Below are some of your previous responses that had issues. I will explain the errors to help you avoid them in the future:\n<do_not_respond_like_this>")
            issues.extend(f"- {issue}" for issue in self._current_session.issues)
            issues.append("</do_not_respond_like_this>")
            issues = "\n".join(issues)
            system_prompt_with_interactions_and_tools_list.append(issues)

        # Response format
        if self.tools or self.interaction:
            response_format = []
            response_format.append("### Your response format will be in the following JSON format:\n<response_format>")
            response_format.append("[{\"name\": \"<name_of_resource>\", \"parameters\": [{\"key\": \"value\"}, ...], \"reasoning\": \"<reasoning>\"} ...]")
            response_format.append("where <name_of_resource> is the name of the agent or tool, [{\"key\": \"value\"}, ...] is a list of parameters for the tool and <reasoning> is the reason why this tool/agent was chosen and why the parameters are what they are. Once you have gathered all necessary information and completed the user's request, use the execution_completed tool to indicate that your execution is finished.")
            response_format.append("</response_format>")
            response_format = "\n".join(response_format)
            system_prompt_with_interactions_and_tools_list.append(response_format)

        # Add examples here
        if self.examples:
            examples = []
            examples.append("### Examples\n<examples>")
            examples.append(self.examples)
            examples.append("</examples>")
            examples = "\n".join(examples)
            system_prompt_with_interactions_and_tools_list.append(examples)

        system_prompt = "\n\n".join(system_prompt_with_interactions_and_tools_list)
        # print(f"\n\n{system_prompt}\n\n")
        return system_prompt


    def execute_collective_intelligence(self, input: str, provide_summary: bool = True, entity_id: str = None) -> str:
        self._update_current_session(entity_id=entity_id)
        execution_finished = False
        self.log("info", f"I am addressing input: '{input:50}'")
        while not execution_finished:
            execution_response_json_str = self._execute(input=input)
            execution_response_json_str_repaired = extract_json(execution_response_json_str)
            try:
                execution_response_json = json.loads(execution_response_json_str_repaired)
                # Execute tools or agents
                for resource in execution_response_json:
                    amount_of_resources_required_executing = len(execution_response_json)
                    resource_required_executing: dict = resource.get("name")
                    parameters_list = resource.get("parameters")
                    reasoning = resource.get("reasoning")
                    # If the function name is the execution_completed function and there is only one resource, then the execution is completed
                    if resource_required_executing == "execution_completed":
                        # If the execution_completed function is the only resource, then the execution is completed, otherwise continue
                        if amount_of_resources_required_executing == 1:
                            execution_finished = True
                            self.log("info", f"I have finished executing because {reasoning}")
                            break
                        continue
                    # If the function name is not the execution_completed function, execute the tool or agent
                    # Execute if the resource is a tool
                    for tool in self.tools:
                        if resource_required_executing == tool.__name__:
                            try:
                                self.log("info", f"I am going to execute tool '{resource_required_executing}' with parameters: {parameters_list} because {reasoning}")
                                # Convert the list of parameter dictionaries into a single dictionary
                                parameters = {}
                                for parameter in parameters_list:
                                    parameters.update(parameter)

                                # Execute the tool with the parameters
                                tool_result = tool(**parameters)

                                # Create a ToolResult instance
                                tool_result_record = ActionResult(
                                    name=tool.__name__,
                                    description=tool.__doc__ or "No description available.",
                                    parameters=parameters,
                                    result=tool_result
                                )

                                # Append the result to the agent's actions
                                self._current_session.actions.append(tool_result_record)
                                self.log("info", f"I was able to execute the '{resource_required_executing}' tool successfully and received the result: {tool_result}")

                            # If there is an error with the tool, raise a ToolError to provide feedback to the agent
                            except Exception as e:
                                    raise ToolError(f"An error occurred with the tool '{resource_required_executing}'. Error: {e}")

                    # Execute if the resource is an agent
                    for agent in self.interaction:
                        if resource_required_executing == agent.name:
                            try:
                                if isinstance(parameters_list, dict):
                                    request = parameters_list.get("request")
                                elif isinstance(parameters_list, list):
                                    request = parameters_list[0].get("request")
                                self.log("info", f"I am going to communicate with '{agent.name}' and will say '{request}' because {reasoning}")
                                agent_response = agent.execute_collective_intelligence(input=request, provide_summary=False, entity_id=self.id)

                                agent_result_record = ActionResult(
                                    name=agent.name,
                                    description=agent.description,
                                    parameters={"request": request},
                                    result=agent_response
                                )

                                self._current_session.actions.append(agent_result_record)
                                self.log("info", f"I was able to communicate with '{agent.name}' successfully and received the result: {agent_response}")
                            except Exception as e:
                                raise AgentError(f"An error occurred with the agent '{resource_required_executing}'. Error: {e}")

            # Here we communicate back to the agent that we had some issues with it's response. This is a way to help the agent learn from it's mistakes
            except json.JSONDecodeError as e:
                # If there is an issue with the JSON formatting, add it to the issues that way the agent can learn from it
                issue = f"Response: {e.doc}, Error: {e}. This error suggests that the response from the agent was not in the correct JSON format. Please ensure that the response is in the correct JSON format."
                self._current_session.issues.append(issue)
                self.log(level="error", message=f"I ran into an issue decoding JSON, I could not decode: {e.doc}\nI ran into a JSONDecodeError. I am going to start again and learn from this mistake.")
                continue

            except ValueError as e:
                issue = f"""Response: You attempted to use the {resource_required_executing} tool with these parameters {resource["parameters"]} and you recevied this error - Error: {e}. This error suggests that there was an issue with the parameters in the response from the agent. Please ensure that the parameters are a list of dictionaries and not just a dictionary."""
                self._current_session.issues.append(issue)
                self.log(level="error", message=f"I ran into an issue running a resource - {resource_required_executing}\nI ran into a value error... I am going to start again and learn from this mistake.")
                continue

            except ToolError as e:
                issue = f"""Response: You attempted to use the {resource_required_executing} tool with these parameters {resource["parameters"]} and you recevied this error - Error: {e}. This error suggests that there was an issue with the tool. Please ensure that you are calling the tool with the correct parameters and types."""
                self._current_session.issues.append(issue)
                self.log(level="error", message=f"I ran into an issue running a resource - {resource_required_executing}\nI am going to start again and learn from this mistake.")
                continue

            except AgentError as e:
                issue = f"""Response: You attempted to use the {resource_required_executing} tool with these parameters {resource["parameters"]} and you recevied this error - Error: {e}. This error suggests that there was an issue with the agent. Please ensure that you are calling the agent with the correct parameters and types."""
                self._current_session.issues.append(issue)
                self.log(level="error", message=f"I ran into an issue running a resource - {resource_required_executing}\nI am going to start again and learn from this mistake.")
                continue

        # At this point we do not know what results we have had, issues we have run into, but we know that the execution has finished, so we aggregate all the information and return a useful response with as much information as possible
        if provide_summary:
            response = self._get_full_summary(input=input)
        else:
            response = self._get_action_summary(input=input, reasoning=reasoning)

        # Respond with the response and session information as a dictionary
        response_with_session = {
            "response": response,
            "entity_id": self._current_session.entity_id,
            "session_id": self._current_session.id,
        }

        # Just returning a string for now
        return response_with_session





