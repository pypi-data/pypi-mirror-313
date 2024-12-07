SMTP Integration
===============

The Shoutbox library provides SMTP support as an alternative to the REST API. This can be useful for legacy systems or environments where SMTP is preferred.

Basic Usage
----------

.. code-block:: python

    from shoutbox import SMTPClient, Email

    # Initialize client
    client = SMTPClient(api_key='your-api-key')

    # Create and send email
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Hello!</h1><p>This is a test email.</p>"
    )

    client.send(email)

Configuration Options
-------------------

The SMTPClient constructor accepts several configuration options:

.. code-block:: python

    client = SMTPClient(
        api_key='your-api-key',
        host='custom.smtp.server',  # default: smtp.shoutbox.net
        port=465,                   # default: 587
        use_tls=True,              # default: True
        timeout=60                  # default: 30
    )

Multiple Recipients
----------------

You can send to multiple recipients:

.. code-block:: python

    email = Email(
        from_email="sender@example.com",
        to=[
            "recipient1@example.com",
            "recipient2@example.com"
        ],
        subject="Group Message",
        html="<h1>Hello Everyone!</h1>"
    )

Named Recipients
-------------

Recipients can include display names:

.. code-block:: python

    from shoutbox import EmailAddress

    email = Email(
        from_email=EmailAddress("sender@example.com", "Sender Name"),
        to=[
            EmailAddress("recipient1@example.com", "John Doe"),
            EmailAddress("recipient2@example.com", "Jane Smith")
        ],
        subject="Group Message",
        html="<h1>Hello Everyone!</h1>"
    )

Attachments
----------

Adding file attachments:

.. code-block:: python

    from shoutbox import Attachment

    # Create attachment
    with open('document.pdf', 'rb') as f:
        attachment = Attachment(
            filename='document.pdf',
            content=f.read(),
            content_type='application/pdf'
        )

    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Document Attached",
        html="<h1>Please find the document attached</h1>",
        attachments=[attachment]
    )

Custom Headers
------------

Adding custom email headers:

.. code-block:: python

    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Priority Message",
        html="<h1>Important!</h1>",
        headers={
            'X-Priority': '1',
            'X-MSMail-Priority': 'High',
            'Importance': 'High'
        }
    )

Error Handling
------------

The SMTP client provides comprehensive error handling:

.. code-block:: python

    from shoutbox import SMTPClient, Email, ShoutboxError

    client = SMTPClient(api_key='your-api-key')

    try:
        email = Email(
            from_email="sender@example.com",
            to="recipient@example.com",
            subject="Test Email",
            html="<h1>Test</h1>"
        )
        success = client.send(email)
    except ShoutboxError as e:
        print(f"SMTP error: {e}")

Context Manager
-------------

The SMTP client can be used as a context manager:

.. code-block:: python

    with SMTPClient(api_key='your-api-key') as client:
        email = Email(
            from_email="sender@example.com",
            to="recipient@example.com",
            subject="Test Email",
            html="<h1>Test</h1>"
        )
        success = client.send(email)

Best Practices
------------

1. **TLS Usage**
    - Always use TLS in production
    - Verify SSL certificates
    - Use secure ports (587/465)

2. **Authentication**
    - Use environment variables for API keys
    - Store credentials securely
    - Never hardcode sensitive data

3. **Error Handling**
    - Always wrap SMTP operations in try/except blocks
    - Log errors appropriately
    - Implement retry mechanisms for transient failures

4. **Resource Management**
    - Use context managers when possible
    - Close connections properly
    - Set appropriate timeouts

5. **Email Content**
    - Validate email addresses
    - Keep attachments reasonably sized
    - Use proper content types
    - Include both HTML and plain text versions when needed
