"""
Test direct API functionality
"""
import os
import base64
import pytest
import requests

def send_test_email(api_key, from_email, to_email):
    """Send a test email using the direct API"""
    data = {
        'from': from_email,
        'to': to_email,
        'subject': 'Test Email via Direct API',
        'html': '<h1>Hello!</h1><p>This is a test email sent directly via the Shoutbox API.</p>',
        'name': 'Sender Name',
        'reply_to': from_email
    }
   
    response = requests.post(
        'https://api.shoutbox.net/send',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    return response

def send_test_email_with_attachment(api_key, from_email, to_email):
    """Send a test email with attachment using direct API"""
    # Create and read test file
    test_content = "This is a test attachment file."
    with open('test.txt', 'w') as f:
        f.write(test_content)
    
    with open('test.txt', 'rb') as f:
        file_content = base64.b64encode(f.read()).decode()

    data = {
        'from': from_email,
        'to': to_email,
        'subject': 'Test Email with Attachment via Direct API',
        'html': '<h1>Hello!</h1><p>This email includes an attachment.</p>',
        'attachments': [{
            'filename': 'test.txt',
            'content': file_content
        }]
    }

    response = requests.post(
        'https://api.shoutbox.net/send',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json=data
    )

    # Clean up test file
    os.remove('test.txt')
    return response

def send_test_email_with_headers(api_key, from_email, to_email):
    """Send a test email with custom headers using direct API"""
    data = {
        'from': from_email,
        'to': to_email,
        'subject': 'Test Email with Custom Headers via Direct API',
        'html': '<h1>Hello!</h1><p>This email includes custom headers.</p>',
        'headers': {
            'X-Custom-Header': 'Custom Value',
            'X-Priority': '1'
        }
    }

    response = requests.post(
        'https://api.shoutbox.net/send',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    return response

@pytest.fixture
def env_vars():
    """Get environment variables needed for tests"""
    api_key = os.environ.get('SHOUTBOX_API_KEY')
    from_email = os.environ.get('SHOUTBOX_FROM')
    to_email = os.environ.get('SHOUTBOX_TO')

    # Verify environment variables are set
    assert api_key, "SHOUTBOX_API_KEY environment variable must be set"
    assert from_email, "SHOUTBOX_FROM environment variable must be set"
    assert to_email, "SHOUTBOX_TO environment variable must be set"

    return api_key, from_email, to_email

def test_send_basic_email(env_vars):
    """Test sending a basic email via direct API"""
    api_key, from_email, to_email = env_vars
    
    # Send test email
    response = send_test_email(api_key, from_email, to_email)
    
    # Verify response
    assert response.status_code == 200, f"API call failed with response: {response.text}"
    response_data = response.json()
    assert 'emailid' in response_data, "Response should contain emailid"
    assert response_data['message'] == "Payload uploaded successfully"

def test_send_email_with_attachment(env_vars):
    """Test sending an email with attachment via direct API"""
    api_key, from_email, to_email = env_vars
    
    # Send test email with attachment
    response = send_test_email_with_attachment(api_key, from_email, to_email)
    
    # Verify response
    assert response.status_code == 200, f"API call failed with response: {response.text}"
    response_data = response.json()
    assert 'emailid' in response_data, "Response should contain emailid"
    assert response_data['message'] == "Payload uploaded successfully"

def test_send_email_with_headers(env_vars):
    """Test sending an email with custom headers via direct API"""
    api_key, from_email, to_email = env_vars
    
    # Send test email with custom headers
    response = send_test_email_with_headers(api_key, from_email, to_email)
    
    # Verify response
    assert response.status_code == 200, f"API call failed with response: {response.text}"
    response_data = response.json()
    assert 'emailid' in response_data, "Response should contain emailid"
    assert response_data['message'] == "Payload uploaded successfully"
