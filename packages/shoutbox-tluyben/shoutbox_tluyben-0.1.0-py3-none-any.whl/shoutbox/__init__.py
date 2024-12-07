"""
Shoutbox Python Library
~~~~~~~~~~~~~~~~~~~~~

A Python library for sending emails through Shoutbox.net.
"""

from .client import ShoutboxClient
from .smtp import SMTPClient
from .models import Email, EmailAddress, Attachment
from .exceptions import ShoutboxError, ValidationError, APIError

__version__ = '0.1.0'

__all__ = [
    'ShoutboxClient',
    'SMTPClient',
    'Email',
    'EmailAddress',
    'Attachment',
    'ShoutboxError',
    'ValidationError',
    'APIError'
]
