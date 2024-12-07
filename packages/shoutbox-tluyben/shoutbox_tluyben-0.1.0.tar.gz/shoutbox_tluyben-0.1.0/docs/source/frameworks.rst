Framework Integration
====================

The Shoutbox library provides seamless integration with popular Python web frameworks.

Flask Integration
--------------

Basic Integration
~~~~~~~~~~~~~~~

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

File Attachments
~~~~~~~~~~~~~~

.. code-block:: python

    @app.route('/send-with-attachment', methods=['POST'])
    def send_with_attachment():
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
                
            file = request.files['file']
            
            attachment = Attachment(
                filename=file.filename,
                content=file.read(),
                content_type=file.content_type
            )
            
            email = Email(
                from_email="your-app@domain.com",
                to=request.form['to'],
                subject=request.form['subject'],
                html=request.form['html'],
                attachments=[attachment]
            )
            
            result = client.send(email)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

Contact Form Example
~~~~~~~~~~~~~~~~~

.. code-block:: python

    @app.route('/contact', methods=['POST'])
    def handle_contact_form():
        try:
            email = Email(
                from_email=EmailAddress(
                    request.form['email'],
                    request.form.get('name', '')
                ),
                to='contact@yourdomain.com',
                subject=f"Contact Form: {request.form['subject']}",
                html=f"""
                    <h2>Contact Form Submission</h2>
                    <p><strong>From:</strong> {request.form.get('name', 'Not provided')}</p>
                    <p><strong>Email:</strong> {request.form['email']}</p>
                    <p><strong>Message:</strong></p>
                    <p>{request.form['message']}</p>
                """
            )
            
            result = client.send(email)
            return jsonify({'message': 'Thank you for your message!'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

Django Integration
---------------

Settings Configuration
~~~~~~~~~~~~~~~~~~~

Add to your Django settings:

.. code-block:: python

    # settings.py
    SHOUTBOX_API_KEY = 'your-api-key'

Email Backend
~~~~~~~~~~~

Create a custom email backend:

.. code-block:: python

    # backends.py
    from django.core.mail.backends.base import BaseEmailBackend
    from shoutbox import ShoutboxClient, Email, EmailAddress
    from django.conf import settings

    class ShoutboxEmailBackend(BaseEmailBackend):
        def __init__(self, fail_silently=False, **kwargs):
            super().__init__(fail_silently=fail_silently)
            self.client = ShoutboxClient(api_key=settings.SHOUTBOX_API_KEY)

        def send_messages(self, email_messages):
            if not email_messages:
                return 0

            num_sent = 0
            for message in email_messages:
                try:
                    email = Email(
                        from_email=message.from_email,
                        to=message.to,
                        subject=message.subject,
                        html=message.body if message.content_subtype == 'html' else f'<pre>{message.body}</pre>'
                    )
                    
                    self.client.send(email)
                    num_sent += 1
                except Exception as e:
                    if not self.fail_silently:
                        raise
            return num_sent

View Example
~~~~~~~~~~

.. code-block:: python

    # views.py
    from django.http import JsonResponse
    from shoutbox import ShoutboxClient, Email

    client = ShoutboxClient()

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

Form Example
~~~~~~~~~~

.. code-block:: python

    # forms.py
    from django import forms

    class ContactForm(forms.Form):
        name = forms.CharField(max_length=100)
        email = forms.EmailField()
        subject = forms.CharField(max_length=200)
        message = forms.CharField(widget=forms.Textarea)
        attachment = forms.FileField(required=False)

    # views.py
    def handle_contact_form(request):
        if request.method == 'POST':
            form = ContactForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    attachments = []
                    if 'attachment' in request.FILES:
                        file = request.FILES['attachment']
                        attachments.append(
                            Attachment(
                                filename=file.name,
                                content=file.read(),
                                content_type=file.content_type
                            )
                        )

                    email = Email(
                        from_email=EmailAddress(
                            form.cleaned_data['email'],
                            form.cleaned_data['name']
                        ),
                        to='contact@yourdomain.com',
                        subject=f"Contact Form: {form.cleaned_data['subject']}",
                        html=f"""
                            <h2>Contact Form Submission</h2>
                            <p><strong>From:</strong> {form.cleaned_data['name']}</p>
                            <p><strong>Email:</strong> {form.cleaned_data['email']}</p>
                            <p><strong>Message:</strong></p>
                            <p>{form.cleaned_data['message']}</p>
                        """,
                        attachments=attachments
                    )
                    
                    client.send(email)
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=400)
            return JsonResponse({'error': form.errors}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

Best Practices
------------

1. **Configuration Management**
    - Use environment variables for API keys
    - Keep sensitive data out of version control
    - Use configuration files for non-sensitive settings

2. **Error Handling**
    - Implement proper error handling
    - Return appropriate HTTP status codes
    - Provide meaningful error messages
    - Log errors for debugging

3. **Security**
    - Validate input data
    - Sanitize HTML content
    - Implement rate limiting
    - Use CSRF protection
    - Validate file uploads

4. **Performance**
    - Use asynchronous sending when possible
    - Implement job queues for bulk sending
    - Cache frequently used data
    - Monitor email sending metrics

5. **Testing**
    - Write unit tests
    - Use mock objects for testing
    - Test error scenarios
    - Validate email content
    - Test file attachments
