class ToolError(Exception):
    """Exception raised for errors related to tool operations."""
    def __init__(self, message="An error occurred with the tool."):
        self.message = message
        super().__init__(self.message)
