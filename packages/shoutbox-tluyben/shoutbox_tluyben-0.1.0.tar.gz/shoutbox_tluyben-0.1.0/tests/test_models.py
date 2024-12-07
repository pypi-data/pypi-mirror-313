"""Tests for the Shoutbox models"""

import os
import pytest
from unittest.mock import patch, Mock, MagicMock

from shoutbox import EmailAddress, Email, Attachment
from shoutbox.exceptions import ValidationError

def test_email_address_validation():
    """Test email address validation"""
    # Valid email
    addr = EmailAddress("test@example.com")
    assert addr.email == "test@example.com"
    
    # Valid email with name
    addr = EmailAddress("Test User <test@example.com>")
    assert addr.email == "test@example.com"
    assert addr.name == "Test User"
    
    # Invalid email
    with pytest.raises(ValidationError):
        EmailAddress("invalid-email")

def test_email_address_string_representation():
    """Test email address string representation"""
    # Email only
    addr = EmailAddress("test@example.com")
    assert str(addr) == "test@example.com"
    
    # Email with name
    addr = EmailAddress("test@example.com", name="Test User")
    assert str(addr) == "Test User <test@example.com>"

def test_attachment_creation():
    """Test attachment creation and serialization"""
    content = b"test content"
    attachment = Attachment(
        filename="test.txt",
        content=content,
        content_type="text/plain"
    )
    
    data = attachment.to_dict()
    assert data['filename'] == "test.txt"
    assert data['content_type'] == "text/plain"
    
    # Test default content type
    attachment = Attachment(filename="test.txt", content=content)
    assert attachment.to_dict()['content_type'] == "application/octet-stream"

def test_email_creation():
    """Test email creation and validation"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    # Basic email with single recipient
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    assert isinstance(email.from_email, EmailAddress)
    assert isinstance(email.to[0], EmailAddress)
    assert email.subject == "Test"
    assert email.html == "<h1>Test</h1>"
    
    # Test serialization with single recipient
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == to_email
    
    # Test with multiple recipients
    to_emails = [to_email, "other@example.com"]
    email = Email(
        from_email=from_email,
        to=to_emails,
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    data = email.to_dict()
    assert data['to'] == ','.join(to_emails)

def test_email_with_attachments():
    """Test email with attachments"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    attachment = Attachment(
        filename="test.txt",
        content=b"test content",
        content_type="text/plain"
    )
    
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test with attachment",
        html="<h1>Test</h1>",
        attachments=[attachment]
    )
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == to_email

def test_email_with_headers():
    """Test email with custom headers"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test with headers",
        html="<h1>Test</h1>",
        headers={
            'X-Custom': 'test',
            'X-Priority': '1'
        }
    )
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == to_email

def test_email_with_reply_to():
    """Test email with reply-to address"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test with reply-to",
        html="<h1>Test</h1>",
        reply_to=from_email  # Use from_email as reply-to for testing
    )
    
    assert isinstance(email.reply_to, EmailAddress)
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == to_email

def test_email_address_conversion():
    """Test various forms of email address input"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    # String email
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert isinstance(email.from_email, EmailAddress)
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == to_email
    
    # Test with multiple recipients
    to_emails = [to_email, "other@example.com"]
    email = Email(
        from_email=from_email,
        to=to_emails,
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    data = email.to_dict()
    assert data['to'] == ','.join(to_emails)
