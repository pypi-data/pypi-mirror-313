"""
Example of using Shoutbox API directly without the client library
"""

import os
import requests
import base64

# Get API key and email addresses from environment variables
api_key = os.getenv('SHOUTBOX_API_KEY', 'your-api-key-here')
from_email = os.getenv('SHOUTBOX_FROM', 'sender@example.com')
to_email = os.getenv('SHOUTBOX_TO', 'recipient@example.com')

def send_basic_email():
    """Send a basic email using direct API calls"""
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

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

def send_email_with_attachment():
    """Send an email with attachment using direct API calls"""
    # Read file content and encode as base64
    with open('examples/test.txt', 'rb') as f:
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

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

def send_email_with_custom_headers():
    """Send an email with custom headers using direct API calls"""
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

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == '__main__':
    # Create test.txt for attachment example
    with open('examples/test.txt', 'w') as f:
        f.write('This is a test attachment file.')

    print("Sending basic email...")
    send_basic_email()

    print("\nSending email with attachment...")
    send_email_with_attachment()

    print("\nSending email with custom headers...")
    send_email_with_custom_headers()
