"""Tests for the Shoutbox SMTP client"""

import os
import pytest
from unittest.mock import patch, Mock, MagicMock
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from shoutbox import SMTPClient, Email, EmailAddress, Attachment
from shoutbox.exceptions import ShoutboxError, ValidationError

def test_smtp_client_initialization():
    """Test SMTP client initialization with API key"""
    # Test with direct API key
    client = SMTPClient(api_key=os.getenv('SHOUTBOX_API_KEY'))
    assert client.api_key == os.getenv('SHOUTBOX_API_KEY')
    
    # Test with environment variable
    client = SMTPClient()
    assert client.api_key == os.getenv('SHOUTBOX_API_KEY')
    
    # Test missing API key
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            SMTPClient()

def test_smtp_client_custom_settings():
    """Test SMTP client with custom settings"""
    client = SMTPClient(
        api_key=os.getenv('SHOUTBOX_API_KEY'),
        host="smtp.shoutbox.net",  # Use actual SMTP server
        port=587,
        use_tls=True,
        timeout=60
    )
    
    assert client.host == "smtp.shoutbox.net"
    assert client.port == 587
    assert client.use_tls is True
    assert client.timeout == 60

def test_send_basic_email():
    """Test sending a basic email via SMTP"""
    client = SMTPClient()
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email via SMTP Client",
        html="<h1>Test</h1><p>This is a test email sent using the SMTP client.</p>"
    )
    
    success = client.send(email)
    assert success is True

def test_send_email_with_attachment():
    """Test sending an email with attachment via SMTP"""
    client = SMTPClient()
    
    # Create test file
    content = b"This is a test attachment from the SMTP client."
    attachment = Attachment(
        filename="test.txt",
        content=content,
        content_type="text/plain"
    )
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email with Attachment via SMTP",
        html="<h1>Test</h1><p>This email includes an attachment.</p>",
        attachments=[attachment]
    )
    
    success = client.send(email)
    assert success is True

def test_send_email_with_multiple_recipients():
    """Test sending an email to multiple recipients via SMTP"""
    client = SMTPClient()
    
    # Split SHOUTBOX_TO into multiple recipients if it contains commas
    to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=to_addresses,
        subject="Test Email with Multiple Recipients via SMTP",
        html="<h1>Test</h1><p>This email is sent to multiple recipients.</p>",
        headers={
            'X-Custom-Header': 'Custom Value',
            'X-Priority': '1'
        }
    )
    
    success = client.send(email)
    assert success is True

@patch('smtplib.SMTP')
def test_smtp_error_handling(mock_smtp):
    """Test SMTP error handling"""
    # Configure mock to raise authentication error
    mock_instance = Mock()
    mock_instance.login.side_effect = smtplib.SMTPAuthenticationError(535, b'Authentication failed')
    mock_smtp.return_value.__enter__.return_value = mock_instance
    
    # Test with invalid credentials
    client = SMTPClient(api_key="invalid-key")
    
    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    with pytest.raises(ShoutboxError):
        client.send(email)
    
    # Test with invalid server
    mock_instance.login.side_effect = smtplib.SMTPServerDisconnected()
    
    client = SMTPClient(
        api_key=os.getenv('SHOUTBOX_API_KEY'),
        host="invalid.smtp.server"
    )
    
    with pytest.raises(ShoutboxError):
        client.send(email)

def test_context_manager():
    """Test SMTP client as context manager"""
    with SMTPClient() as client:
        assert isinstance(client, SMTPClient)
        
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=os.getenv('SHOUTBOX_TO'),
            subject="Test Email via SMTP Context Manager",
            html="<h1>Test</h1><p>This email was sent using a context manager.</p>"
        )
        
        success = client.send(email)
        assert success is True
