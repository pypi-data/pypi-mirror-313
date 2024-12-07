"""
Test Shoutbox API Client functionality
"""
import os
import json
import pytest
from shoutbox import ShoutboxClient, Email, EmailAddress

@pytest.fixture
def client():
    """Create a ShoutboxClient instance"""
    return ShoutboxClient()

def test_send_basic_email(client):
    """Test sending a basic email using the API client"""
    # Get environment variables directly like in the example
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')

    print(f"\nFrom: {from_email}")
    print(f"To: {to_email}")

    # Create email exactly like in the example
    email = Email(
        from_email=EmailAddress(from_email, "Sender Name"),
        to=to_email,
        subject="Test Email via API Client",
        html="<h1>Hello!</h1><p>This is a test email sent using the Shoutbox API Client.</p>",
        reply_to=from_email
    )

    # Print the payload that will be sent
    payload = email.to_dict()
    print("\nPayload being sent:")
    print(json.dumps(payload, indent=2))

    # Send email using the client
    response = client.send(email)
    assert response, "Should receive a response"
    assert 'emailid' in response, "Response should have emailid"
    assert response['message'] == "Payload uploaded successfully"
