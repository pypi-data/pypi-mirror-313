API Reference
=============

This section provides detailed documentation for the Shoutbox Python library's API.

ShoutboxClient
------------

.. code-block:: python

    from shoutbox import ShoutboxClient

The main client for interacting with the Shoutbox API.

.. py:class:: ShoutboxClient(api_key: str = None, base_url: str = "https://api.shoutbox.net", timeout: int = 30, verify_ssl: bool = True)

    :param api_key: Your Shoutbox API key (can be set via SHOUTBOX_API_KEY env var)
    :param base_url: API base URL
    :param timeout: Request timeout in seconds
    :param verify_ssl: Whether to verify SSL certificates

    .. py:method:: send(email: Email) -> dict

        Send an email using the Shoutbox API

        :param email: Email object containing the email details
        :returns: API response as dictionary
        :raises ValidationError: If email validation fails
        :raises APIError: If the API request fails
        :raises ShoutboxError: For other Shoutbox-related errors

SMTPClient
---------

.. code-block:: python

    from shoutbox import SMTPClient

Client for sending emails via SMTP.

.. py:class:: SMTPClient(api_key: str = None, host: str = "smtp.shoutbox.net", port: int = 587, use_tls: bool = True, timeout: int = 30)

    :param api_key: Your Shoutbox API key (can be set via SHOUTBOX_API_KEY env var)
    :param host: SMTP server hostname
    :param port: SMTP server port
    :param use_tls: Whether to use TLS
    :param timeout: Connection timeout in seconds

    .. py:method:: send(email: Email) -> bool

        Send an email using the Shoutbox SMTP service

        :param email: Email object containing the email details
        :returns: True if email was sent successfully
        :raises ValidationError: If email validation fails
        :raises ShoutboxError: For SMTP-related errors

Email
-----

.. code-block:: python

    from shoutbox import Email

Class representing an email message.

.. py:class:: Email(to: Union[str, list[str], EmailAddress, list[EmailAddress]], subject: str, html: str, from_email: Optional[Union[str, EmailAddress]] = None, reply_to: Optional[Union[str, EmailAddress]] = None, headers: Optional[dict] = None, attachments: Optional[list[Attachment]] = None)

    :param to: Recipient email address(es)
    :param subject: Email subject
    :param html: HTML content of the email
    :param from_email: Sender's email address
    :param reply_to: Reply-to email address
    :param headers: Custom email headers
    :param attachments: List of attachments

EmailAddress
----------

.. code-block:: python

    from shoutbox import EmailAddress

Class representing an email address with optional display name.

.. py:class:: EmailAddress(email: str, name: Optional[str] = None)

    :param email: Email address
    :param name: Display name (optional)

Attachment
---------

.. code-block:: python

    from shoutbox import Attachment

Class representing an email attachment.

.. py:class:: Attachment(filename: str, content: bytes, content_type: Optional[str] = None)

    :param filename: Name of the file
    :param content: File content as bytes
    :param content_type: MIME type of the file

Exceptions
---------

.. code-block:: python

    from shoutbox.exceptions import ShoutboxError, ValidationError, APIError

Base Exceptions
~~~~~~~~~~~~~

.. py:exception:: ShoutboxError

    Base exception for all Shoutbox-related errors

Specific Exceptions
~~~~~~~~~~~~~~~~

.. py:exception:: ValidationError

    Raised when input validation fails

.. py:exception:: APIError(message: str, status_code: int, response_body: dict = None)

    Raised when the API returns an error response

    :param message: Error message
    :param status_code: HTTP status code
    :param response_body: API response body

Usage Examples
------------

Basic Usage
~~~~~~~~~

.. code-block:: python

    from shoutbox import ShoutboxClient, Email

    client = ShoutboxClient(api_key='your-api-key')

    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Hello!</h1>"
    )

    try:
        response = client.send(email)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

With Attachments
~~~~~~~~~~~~~

.. code-block:: python

    from shoutbox import ShoutboxClient, Email, Attachment

    client = ShoutboxClient(api_key='your-api-key')

    with open('document.pdf', 'rb') as f:
        attachment = Attachment(
            filename='document.pdf',
            content=f.read(),
            content_type='application/pdf'
        )

    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Document",
        html="<h1>Please find the document attached</h1>",
        attachments=[attachment]
    )

    client.send(email)

With Custom Headers
~~~~~~~~~~~~~~~

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

Error Handling
~~~~~~~~~~~

.. code-block:: python

    try:
        response = client.send(email)
    except ValidationError as e:
        print(f"Validation error: {e}")
    except APIError as e:
        print(f"API error (status {e.status_code}): {e}")
    except ShoutboxError as e:
        print(f"General error: {e}")

Context Managers
~~~~~~~~~~~~~

Both clients support context managers:

.. code-block:: python

    with ShoutboxClient(api_key='your-key') as client:
        client.send(email)

    with SMTPClient(api_key='your-key') as client:
        client.send(email)
