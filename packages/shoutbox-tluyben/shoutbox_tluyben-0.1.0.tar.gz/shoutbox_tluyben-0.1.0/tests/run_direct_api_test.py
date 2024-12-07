"""
Simple test runner for direct API - with detailed request info
"""
import os
import requests
import json

# Get API key and email addresses from environment variables
api_key = os.getenv('SHOUTBOX_API_KEY', 'your-api-key-here')
from_email = os.getenv('SHOUTBOX_FROM', 'sender@example.com')
to_email = os.getenv('SHOUTBOX_TO', 'recipient@example.com')

print(f"API Key: {api_key}")
print(f"From: {from_email}")
print(f"To: {to_email}")

print("Running direct API test...")

data = {
    'from': from_email,
    'to': to_email,
    'subject': 'Test Email via Direct API',
    'html': '<h1>Hello!</h1><p>This is a test email sent directly via the Shoutbox API.</p>',
    'name': 'Sender Name',
    'reply_to': from_email
}

print("\nRequest data:")
print(json.dumps(data, indent=2))

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
print("\nRequest headers:")
print(json.dumps(headers, indent=2))

response = requests.post(
    'https://api.shoutbox.net/send',
    headers=headers,
    json=data
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")
