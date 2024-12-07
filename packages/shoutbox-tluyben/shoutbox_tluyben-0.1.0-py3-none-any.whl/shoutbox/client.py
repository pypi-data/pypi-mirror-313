"""
Shoutbox client
~~~~~~~~~~~~~

This module contains the Shoutbox client class.
"""

import os
from urllib.parse import urlparse
import requests

from .models import Email
from .exceptions import ShoutboxError, APIError

class ShoutboxClient:
    """Client for the Shoutbox email API"""
    
    def __init__(
        self, 
        api_key: str = None,
        base_url: str = "https://api.shoutbox.net",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv('SHOUTBOX_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in SHOUTBOX_API_KEY environment variable")
        
        # Validate and normalize base URL
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid base URL")
        self.base_url = base_url.rstrip('/')
        
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def send(self, email: Email) -> dict:
        """
        Send an email using the Shoutbox API
        
        Args:
            email: Email object containing the email details
            
        Returns:
            dict: API response
            
        Raises:
            ValidationError: If email validation fails
            APIError: If the API request fails
            ShoutboxError: For other Shoutbox-related errors
        """
        try:
            response = self.session.post(
                f"{self.base_url}/send",
                json=email.to_dict(),
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            if response.status_code >= 400:
                try:
                    error_body = response.json()
                except ValueError:
                    error_body = response.text
                raise APIError(
                    f"API request failed: {response.text}",
                    response.status_code,
                    error_body
                )
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise ShoutboxError("Request timed out")
        except requests.exceptions.SSLError:
            raise ShoutboxError("SSL verification failed")
        except requests.exceptions.ConnectionError:
            raise ShoutboxError("Connection error")
        except Exception as e:
            if isinstance(e, APIError):
                raise
            raise ShoutboxError(f"Unexpected error: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
