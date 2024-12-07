"""
Example of Django integration with Shoutbox

Directory structure for a Django project:

myproject/
    myproject/
        __init__.py
        settings.py (add settings below)
        urls.py (add URLs below)
    myapp/
        __init__.py
        backends.py (email backend below)
        views.py (views below)
        forms.py (forms below)
"""

# settings.py
"""
# Add to your Django settings.py:

import os

SHOUTBOX_API_KEY = os.getenv('SHOUTBOX_API_KEY')
SHOUTBOX_FROM = os.getenv('SHOUTBOX_FROM')
SHOUTBOX_TO = os.getenv('SHOUTBOX_TO')

EMAIL_BACKEND = 'myapp.backends.ShoutboxEmailBackend'
"""

# backends.py
from django.core.mail.backends.base import BaseEmailBackend
from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment
from django.conf import settings

class ShoutboxEmailBackend(BaseEmailBackend):
    """Custom email backend for Shoutbox"""
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.client = ShoutboxClient(api_key=settings.SHOUTBOX_API_KEY)

    def send_messages(self, email_messages):
        """Send messages using Shoutbox API"""
        if not email_messages:
            return 0

        num_sent = 0
        for message in email_messages:
            try:
                # Convert Django email message to Shoutbox email
                email = Email(
                    from_email=message.from_email or settings.SHOUTBOX_FROM,
                    to=[addr for addr in message.to] or [settings.SHOUTBOX_TO],
                    subject=message.subject,
                    html=message.body if message.content_subtype == 'html' else f'<pre>{message.body}</pre>'
                )

                # Add attachments if any
                if message.attachments:
                    email.attachments = []
                    for attachment in message.attachments:
                        if isinstance(attachment, tuple):
                            filename, content, mimetype = attachment
                            email.attachments.append(
                                Attachment(
                                    filename=filename,
                                    content=content.encode() if isinstance(content, str) else content,
                                    content_type=mimetype
                                )
                            )

                # Send the email
                self.client.send(email)
                num_sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise
        return num_sent

# forms.py
from django import forms

class ContactForm(forms.Form):
    """Example contact form"""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField(required=False)

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm

def send_basic_email(request):
    """Example view for sending a basic email"""
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            settings.SHOUTBOX_FROM,
            [settings.SHOUTBOX_TO],
            html_message='<h1>Test Email</h1><p>This is a test email.</p>'
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def send_email_with_attachment(request):
    """Example view for sending an email with attachment"""
    try:
        message = EmailMessage(
            'Test Email with Attachment',
            '<h1>Test Email</h1><p>This email has an attachment.</p>',
            settings.SHOUTBOX_FROM,
            [settings.SHOUTBOX_TO]
        )
        message.content_subtype = 'html'
        
        # Add attachment
        message.attach('test.txt', 'This is a test file.', 'text/plain')
        
        message.send()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def handle_contact_form(request):
    """Example view for handling contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create email message
                message = EmailMessage(
                    f"Contact Form: {form.cleaned_data['subject']}",
                    f"""
                    <h2>Contact Form Submission</h2>
                    <p><strong>From:</strong> {form.cleaned_data['name']} ({form.cleaned_data['email']})</p>
                    <p><strong>Message:</strong></p>
                    <p>{form.cleaned_data['message']}</p>
                    """,
                    form.cleaned_data['email'],
                    [settings.SHOUTBOX_FROM],  # Send to SHOUTBOX_FROM as contact email
                    reply_to=[form.cleaned_data['email']]
                )
                message.content_subtype = 'html'
                
                # Add attachment if provided
                if 'attachment' in request.FILES:
                    file = request.FILES['attachment']
                    message.attach(file.name, file.read(), file.content_type)
                
                message.send()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# urls.py
"""
# Add to your Django urls.py:

from django.urls import path
from myapp import views

urlpatterns = [
    path('send-email/', views.send_basic_email, name='send_email'),
    path('send-email-with-attachment/', views.send_email_with_attachment, name='send_email_with_attachment'),
    path('contact/', views.handle_contact_form, name='contact_form'),
]
"""

"""
Example usage:

# Basic email
curl -X POST http://localhost:8000/send-email/

# Email with attachment
curl -X POST http://localhost:8000/send-email-with-attachment/

# Contact form
curl -X POST http://localhost:8000/contact/ \
    -F "name=John Doe" \
    -F "email=john@example.com" \
    -F "subject=Test Contact" \
    -F "message=This is a test message" \
    -F "attachment=@/path/to/file.pdf"
"""
