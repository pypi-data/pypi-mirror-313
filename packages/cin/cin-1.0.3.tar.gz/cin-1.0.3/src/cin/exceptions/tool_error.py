class AgentError(Exception):
    """Exception raised for errors related to agent operations."""
    def __init__(self, message="An error occurred with the agent."):
        self.message = message
        super().__init__(self.message)