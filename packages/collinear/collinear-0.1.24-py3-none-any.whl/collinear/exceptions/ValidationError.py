from typing import Union, List


class ValidationError(Exception):
    """Exception raised for errors in the input validation."""
    def __init__(self, message: str, example: Union[dict, List[dict]] = None):
        super().__init__(message)
        self.example = example