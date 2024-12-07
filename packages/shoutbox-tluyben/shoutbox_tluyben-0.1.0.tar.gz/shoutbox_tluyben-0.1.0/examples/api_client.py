"""
Example of using Shoutbox API Client
"""

import os
from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment

def send_basic_email():
    """Send a basic email using the API client"""
    client = ShoutboxClient()

    email = Email(
        from_email=EmailAddress(os.getenv('SHOUTBOX_FROM'), "Sender Name"),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email via API Client",
        html="<h1>Hello!</h1><p>This is a test email sent using the Shoutbox API Client.</p>",
        reply_to=os.getenv('SHOUTBOX_FROM')
    )

    try:
        response = client.send(email)
        print("Basic email sent successfully!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_attachment():
    """Send an email with attachment using the API client"""
    client = ShoutboxClient()

    # Read file content
    with open('examples/test.txt', 'rb') as f:
        content = f.read()

    # Create attachment
    attachment = Attachment(
        filename='test.txt',
        content=content,
        content_type='text/plain'
    )

    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email with Attachment",
        html="<h1>Hello!</h1><p>This email includes an attachment.</p>",
        attachments=[attachment]
    )

    try:
        response = client.send(email)
        print("Email with attachment sent successfully!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_multiple_recipients():
    """Send an email to multiple recipients using the API client"""
    client = ShoutboxClient()

    # Split SHOUTBOX_TO into multiple recipients if it contains commas
    to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]

    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=to_addresses,
        subject="Test Email with Multiple Recipients",
        html="<h1>Hello!</h1><p>This email is sent to multiple recipients.</p>",
        headers={
            'X-Custom-Header': 'Custom Value',
            'X-Priority': '1'
        }
    )

    try:
        response = client.send(email)
        print("Email to multiple recipients sent successfully!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_named_recipients():
    """Send an email with named recipients using the API client"""
    client = ShoutboxClient()

    # Split SHOUTBOX_TO into multiple recipients if it contains commas
    to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]

    email = Email(
        from_email=EmailAddress(os.getenv('SHOUTBOX_FROM'), "Sender Name"),
        to=[
            EmailAddress(addr, f"Recipient {i+1}")
            for i, addr in enumerate(to_addresses)
        ],
        subject="Test Email with Named Recipients",
        html="<h1>Hello!</h1><p>This email is sent to recipients with display names.</p>"
    )

    try:
        response = client.send(email)
        print("Email with named recipients sent successfully!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    # Create test.txt for attachment example
    with open('examples/test.txt', 'w') as f:
        f.write('This is a test attachment file.')

    print("Sending basic email...")
    send_basic_email()

    print("\nSending email with attachment...")
    send_email_with_attachment()

    print("\nSending email with multiple recipients...")
    send_email_with_multiple_recipients()

    print("\nSending email with named recipients...")
    send_email_with_named_recipients()
