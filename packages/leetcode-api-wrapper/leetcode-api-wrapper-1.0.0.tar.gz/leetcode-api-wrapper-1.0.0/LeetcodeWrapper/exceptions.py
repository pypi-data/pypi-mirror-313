class APIError(Exception):
    """Exception raised for errors in the API response.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="An error occurred with the API"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Exception raised for validation errors in input parameters.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Invalid input parameter"):
        self.message = message
        super().__init__(self.message)
