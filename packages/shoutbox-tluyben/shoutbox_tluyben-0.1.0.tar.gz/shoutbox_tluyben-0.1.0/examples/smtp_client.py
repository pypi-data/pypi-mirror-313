"""
Example of using Shoutbox SMTP Client
"""

import os
from shoutbox import SMTPClient, Email, EmailAddress, Attachment

def send_basic_email():
    """Send a basic email using the SMTP client"""
    client = SMTPClient()

    email = Email(
        from_email=EmailAddress(os.getenv('SHOUTBOX_FROM'), "Sender Name"),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email via SMTP Client",
        html="<h1>Hello!</h1><p>This is a test email sent using the Shoutbox SMTP Client.</p>",
        reply_to=os.getenv('SHOUTBOX_FROM')
    )

    try:
        success = client.send(email)
        print("Basic email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_attachment():
    """Send an email with attachment using the SMTP client"""
    client = SMTPClient()

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
        subject="Test Email with Attachment via SMTP",
        html="<h1>Hello!</h1><p>This email includes an attachment.</p>",
        attachments=[attachment]
    )

    try:
        success = client.send(email)
        print("Email with attachment sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_multiple_recipients():
    """Send an email to multiple recipients using the SMTP client"""
    client = SMTPClient()

    # Split SHOUTBOX_TO into multiple recipients if it contains commas
    to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]

    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=to_addresses,
        subject="Test Email with Multiple Recipients via SMTP",
        html="<h1>Hello!</h1><p>This email is sent to multiple recipients.</p>",
        headers={
            'X-Custom-Header': 'Custom Value',
            'X-Priority': '1'
        }
    )

    try:
        success = client.send(email)
        print("Email to multiple recipients sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_named_recipients():
    """Send an email with named recipients using the SMTP client"""
    client = SMTPClient()

    # Split SHOUTBOX_TO into multiple recipients if it contains commas
    to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]

    email = Email(
        from_email=EmailAddress(os.getenv('SHOUTBOX_FROM'), "Sender Name"),
        to=[
            EmailAddress(addr, f"Recipient {i+1}")
            for i, addr in enumerate(to_addresses)
        ],
        subject="Test Email with Named Recipients via SMTP",
        html="<h1>Hello!</h1><p>This email is sent to recipients with display names.</p>"
    )

    try:
        success = client.send(email)
        print("Email with named recipients sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_email_with_custom_smtp_settings():
    """Send an email using custom SMTP settings"""
    client = SMTPClient(
        host="custom.smtp.server",
        port=465,
        use_tls=True,
        timeout=60
    )

    email = Email(
        from_email=os.getenv('SHOUTBOX_FROM'),
        to=os.getenv('SHOUTBOX_TO'),
        subject="Test Email with Custom SMTP Settings",
        html="<h1>Hello!</h1><p>This email was sent using custom SMTP settings.</p>"
    )

    try:
        success = client.send(email)
        print("Email with custom SMTP settings sent successfully!")
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

    print("\nSending email with custom SMTP settings...")
    send_email_with_custom_smtp_settings()
