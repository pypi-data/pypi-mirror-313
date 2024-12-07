"""Tests for the Shoutbox API client"""

import os
import pytest
from unittest.mock import patch, Mock

from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment
from shoutbox.exceptions import ShoutboxError, ValidationError, APIError

def test_client_initialization():
    """Test client initialization with API key"""
    # Test with direct API key
    client = ShoutboxClient(api_key=os.getenv('SHOUTBOX_API_KEY'))
    assert client.api_key == os.getenv('SHOUTBOX_API_KEY')
    
    # Test with environment variable
    client = ShoutboxClient()
    assert client.api_key == os.getenv('SHOUTBOX_API_KEY')
    
    # Test missing API key
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            ShoutboxClient()

def test_send_basic_email():
    """Test sending a basic email"""
    client = ShoutboxClient()
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email via API Client",
        html="<h1>Test</h1><p>This is a test email sent using the API client.</p>"
    )
    
    response = client.send(email)
    assert response is not None
    assert isinstance(response, dict)

def test_send_email_with_attachment():
    """Test sending an email with attachment"""
    client = ShoutboxClient()
    
    # Create test file
    content = b"This is a test attachment from the API client."
    attachment = Attachment(
        filename="test.txt",
        content=content,
        content_type="text/plain"
    )
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email with Attachment via API Client",
        html="<h1>Test</h1><p>This email includes an attachment.</p>",
        attachments=[attachment]
    )
    
    response = client.send(email)
    assert response is not None
    assert isinstance(response, dict)

def test_send_email_with_custom_headers():
    """Test sending an email with custom headers"""
    client = ShoutboxClient()
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email with Headers via API Client",
        html="<h1>Test</h1><p>This email includes custom headers.</p>",
        headers={
            'X-Custom': 'test',
            'X-Priority': '1'
        }
    )
    
    response = client.send(email)
    assert response is not None
    assert isinstance(response, dict)

def test_api_error_handling():
    """Test API error handling"""
    client = ShoutboxClient()
    
    # Test with invalid email address
    with pytest.raises(ValidationError):
        email = Email(
            from_email="invalid-email",  # Invalid email to trigger error
            to=os.getenv('SHOUTBOX_TO'),
            subject="Test Email",
            html="<h1>Test</h1>"
        )
    
    # Test with invalid API key
    client = ShoutboxClient(api_key="invalid-key")
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    with pytest.raises(APIError):
        client.send(email)

def test_context_manager():
    """Test client as context manager"""
    with ShoutboxClient() as client:
        assert isinstance(client, ShoutboxClient)
        
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=os.getenv('SHOUTBOX_TO'),
            subject="Test Email via Context Manager",
            html="<h1>Test</h1><p>This email was sent using a context manager.</p>"
        )
        
        response = client.send(email)
        assert response is not None
        assert isinstance(response, dict)
