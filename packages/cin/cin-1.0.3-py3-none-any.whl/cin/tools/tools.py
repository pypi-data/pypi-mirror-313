import inspect
import json


def extract_tool_info(func_list: list[callable]) -> str:
    # Prepare a list to hold all JSON outputs for better control
    function_information_list = []

    for func in func_list:
        # Get the docstring
        docstring = inspect.getdoc(func)

        # Create a dictionary with the extracted information
        func_info = {
            "name": func.__name__,
            "description": docstring,
        }

        # Check if the function has a docstring, throw an error if it does not
        if func_info["description"] is None:
            raise ValueError(f"Function '{func_info['name']}' does not have a docstring.")

        # Convert the dictionary to a JSON-formatted string
        json_output = json.dumps(func_info, indent=4)
        function_information_list.append(json_output)

    # Join all JSON outputs with double newlines for better readability
    return "\n\n".join(function_information_list)

def execution_completed() -> str:
    """
    Returns a message indicating that there are no other tools or agents to call as we have the information we need.

    Parameters:
        None

    Returns:
        str: A message indicating that the execution has been completed.
    """
    return "Execution completed!"

