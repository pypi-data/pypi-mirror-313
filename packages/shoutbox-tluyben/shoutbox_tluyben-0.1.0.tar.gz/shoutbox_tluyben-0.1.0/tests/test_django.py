"""Tests for Django integration"""

import os
import json
import pytest
from django.test import RequestFactory
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

from shoutbox import ShoutboxClient, Email

# Configure Django settings before running tests
if not settings.configured:
    settings.configure(
        DEFAULT_CHARSET='utf-8',
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
        EMAIL_HOST='mail.shoutbox.net',
        EMAIL_PORT=587,
        EMAIL_USE_TLS=True,
        EMAIL_HOST_USER=os.getenv('SHOUTBOX_API_KEY'),
        EMAIL_HOST_PASSWORD=os.getenv('SHOUTBOX_API_KEY'),
        SECRET_KEY='dummy-key-for-tests'
    )

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_basic_email_view(request_factory):
    """Test basic email sending view"""
    def send_email_view(request):
        try:
            send_mail(
                'Test Email via Django Integration',
                'This is a test email.',
                os.getenv('SHOUTBOX_FROM'),
                [os.getenv('SHOUTBOX_TO')],
                html_message='<h1>Test</h1><p>This is a test email sent through Django.</p>'
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    request = request_factory.post('/send-email')
    response = send_email_view(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['success'] is True

def test_email_with_attachment_view(request_factory):
    """Test email sending with attachment"""
    def send_with_attachment_view(request):
        try:
            # Create test message
            message = EmailMessage(
                'Test Email with Attachment via Django',
                '<h1>Test</h1><p>This email includes an attachment.</p>',
                os.getenv('SHOUTBOX_FROM'),
                [os.getenv('SHOUTBOX_TO')]
            )
            message.content_subtype = 'html'
            
            # Add attachment
            message.attach('test.txt', 'This is a test attachment from Django.', 'text/plain')
            
            # Send message
            message.send()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    request = request_factory.post('/send-with-attachment')
    response = send_with_attachment_view(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['success'] is True

def test_bulk_email_view(request_factory):
    """Test bulk email sending"""
    def send_bulk_view(request):
        try:
            # Split SHOUTBOX_TO into multiple recipients if it contains commas
            to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]
            
            message = EmailMessage(
                'Test Bulk Email via Django',
                '<h1>Test</h1><p>This is a bulk test email.</p>',
                os.getenv('SHOUTBOX_FROM'),
                to_addresses
            )
            message.content_subtype = 'html'
            
            # Send message
            message.send()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    request = request_factory.post('/send-bulk')
    response = send_bulk_view(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['success'] is True

def test_error_handling_view(request_factory):
    """Test error handling in Django integration"""
    def error_view(request):
        try:
            # Try to send with invalid email
            send_mail(
                'Test Error Handling',
                'This should fail.',
                'invalid-email',  # Invalid email to trigger error
                [os.getenv('SHOUTBOX_TO')]
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    request = request_factory.post('/send-error')
    response = error_view(request)
    assert response.status_code == 400
    data = json.loads(response.content)
    assert data['success'] is False

def test_custom_backend_view(request_factory):
    """Test using custom email backend"""
    class ShoutboxEmailBackend(BaseEmailBackend):
        def __init__(self, fail_silently=False, **kwargs):
            super().__init__(fail_silently=fail_silently)
            self.client = ShoutboxClient()
        
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
    
    def send_with_backend_view(request):
        try:
            with ShoutboxEmailBackend() as backend:
                message = EmailMessage(
                    'Test Email via Custom Backend',
                    '<h1>Test</h1><p>This email was sent using a custom backend.</p>',
                    os.getenv('SHOUTBOX_FROM'),
                    [os.getenv('SHOUTBOX_TO')]
                )
                message.content_subtype = 'html'
                backend.send_messages([message])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    request = request_factory.post('/send-with-backend')
    response = send_with_backend_view(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['success'] is True
