"""Pytest configuration file"""

import os
import pytest
import subprocess

@pytest.fixture(autouse=True)
def setup_env():
    """Ensure environment variables are set from .env file"""
    result = subprocess.run(
        ['bash', '-c', 'source .env && env'],
        capture_output=True,
        text=True
    )
    for line in result.stdout.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value

@pytest.fixture
def api_client():
    """Create a test API client"""
    from shoutbox import ShoutboxClient
    return ShoutboxClient()

@pytest.fixture
def smtp_client():
    """Create a test SMTP client"""
    from shoutbox import SMTPClient
    return SMTPClient()

@pytest.fixture
def sample_email():
    """Create a sample email for testing"""
    from shoutbox import Email
    return Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email",
        html="<h1>Test</h1>"
    )

@pytest.fixture
def sample_attachment():
    """Create a sample attachment for testing"""
    from shoutbox import Attachment
    return Attachment(
        filename="test.txt",
        content=b"test content",
        content_type="text/plain"
    )

@pytest.fixture
def sample_email_with_attachment(sample_email, sample_attachment):
    """Create a sample email with attachment for testing"""
    sample_email.attachments = [sample_attachment]
    return sample_email
