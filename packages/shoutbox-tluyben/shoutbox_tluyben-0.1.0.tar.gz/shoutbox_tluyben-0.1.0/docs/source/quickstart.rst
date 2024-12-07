Quick Start Guide
===============

This guide will help you get started with the Shoutbox Python library.

Installation
-----------

Install using pip:

.. code-block:: bash

    pip install shoutbox

Basic Usage
----------

Using the API Client
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from shoutbox import ShoutboxClient, Email

    # Initialize client
    client = ShoutboxClient(api_key='your-api-key')

    # Create and send a basic email
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Hello!</h1><p>This is a test email.</p>"
    )

    try:
        response = client.send(email)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

Using the SMTP Client
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from shoutbox import SMTPClient, Email

    # Initialize SMTP client
    client = SMTPClient(api_key='your-api-key')

    # Create and send a basic email
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email via SMTP",
        html="<h1>Hello!</h1><p>This is a test email via SMTP.</p>"
    )

    try:
        success = client.send(email)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

Adding Attachments
---------------

.. code-block:: python

    from shoutbox import ShoutboxClient, Email, Attachment

    client = ShoutboxClient(api_key='your-api-key')

    # Create attachment
    with open('document.pdf', 'rb') as f:
        attachment = Attachment(
            filename='document.pdf',
            content=f.read(),
            content_type='application/pdf'
        )

    # Create email with attachment
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Document Attached",
        html="<h1>Please find the document attached</h1>",
        attachments=[attachment]
    )

    client.send(email)

Multiple Recipients
----------------

.. code-block:: python

    from shoutbox import ShoutboxClient, Email, EmailAddress

    client = ShoutboxClient(api_key='your-api-key')

    # Send to multiple recipients with display names
    email = Email(
        from_email=EmailAddress("sender@example.com", "Sender Name"),
        to=[
            EmailAddress("recipient1@example.com", "John Doe"),
            EmailAddress("recipient2@example.com", "Jane Smith")
        ],
        subject="Group Message",
        html="<h1>Hello Everyone!</h1>"
    )

    client.send(email)

Custom Headers
------------

.. code-block:: python

    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Priority Message",
        html="<h1>Important!</h1>",
        headers={
            'X-Priority': '1',
            'X-Custom-Header': 'Value'
        }
    )

Flask Integration
--------------

.. code-block:: python

    from flask import Flask, request, jsonify
    from shoutbox import ShoutboxClient, Email

    app = Flask(__name__)
    client = ShoutboxClient(api_key='your-api-key')

    @app.route('/send-email', methods=['POST'])
    def send_email():
        try:
            email = Email(
                from_email="your-app@domain.com",
                to=request.json['to'],
                subject=request.json['subject'],
                html=request.json['html']
            )
            
            result = client.send(email)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

Django Integration
---------------

.. code-block:: python

    from django.http import JsonResponse
    from shoutbox import ShoutboxClient, Email

    client = ShoutboxClient(api_key='your-api-key')

    def send_notification(request):
        try:
            email = Email(
                from_email="your-app@domain.com",
                to="recipient@example.com",
                subject="Notification",
                html="<h1>New notification</h1>"
            )
            
            client.send(email)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

Error Handling
------------

.. code-block:: python

    from shoutbox import ShoutboxClient, Email
    from shoutbox.exceptions import ShoutboxError, ValidationError, APIError

    client = ShoutboxClient(api_key='your-api-key')

    try:
        email = Email(
            from_email="sender@example.com",
            to="recipient@example.com",
            subject="Test Email",
            html="<h1>Test</h1>"
        )
        response = client.send(email)
    except ValidationError as e:
        print(f"Validation error: {e}")
    except APIError as e:
        print(f"API error (status {e.status_code}): {e}")
    except ShoutboxError as e:
        print(f"General error: {e}")

Best Practices
------------

1. **API Key Management**
    - Use environment variables:

    .. code-block:: python

        import os
        from shoutbox import ShoutboxClient

        client = ShoutboxClient(api_key=os.getenv('SHOUTBOX_API_KEY'))

2. **Resource Management**
    - Use context managers:

    .. code-block:: python

        with ShoutboxClient(api_key='your-key') as client:
            client.send(email)

3. **Error Handling**
    - Always use try/except blocks
    - Handle specific exceptions
    - Log errors appropriately

4. **File Operations**
    - Use context managers for files
    - Handle large files appropriately
    - Clean up temporary files

5. **Security**
    - Validate email addresses
    - Sanitize HTML content
    - Use HTTPS/TLS
    - Keep API keys secure
