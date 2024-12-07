"""
Shoutbox exceptions
~~~~~~~~~~~~~~~~~

This module contains the set of Shoutbox's exceptions.
"""

class ShoutboxError(Exception):
    """Base exception for Shoutbox API errors"""
    pass

class ValidationError(ShoutboxError):
    """Raised when input validation fails"""
    pass

class APIError(ShoutboxError):
    """Raised when the API returns an error response"""
    def __init__(self, message: str, status_code: int, response_body: dict = None):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)
