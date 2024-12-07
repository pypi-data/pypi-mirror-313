"""Tests for Flask integration"""

import os
import pytest
import json
from flask import Flask, request, jsonify
from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment

@pytest.fixture
def app():
    """Create Flask test app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()

def test_basic_email_endpoint(app, client):
    """Test basic email sending endpoint"""
    # Set up route
    shoutbox = ShoutboxClient()
    
    @app.route('/send-email', methods=['POST'])
    def send_email():
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=os.getenv('SHOUTBOX_TO'),
            subject="Test Email via Flask Integration",
            html="<h1>Test</h1><p>This is a test email sent through Flask.</p>"
        )
        
        response = shoutbox.send(email)
        return jsonify({'success': True, 'response': response})
    
    # Test endpoint
    response = client.post('/send-email')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_email_with_attachment_endpoint(app, client):
    """Test email sending with attachment"""
    shoutbox = ShoutboxClient()
    
    @app.route('/send-with-attachment', methods=['POST'])
    def send_with_attachment():
        # Create test file content
        content = b"This is a test attachment from Flask."
        attachment = Attachment(
            filename="test.txt",
            content=content,
            content_type="text/plain"
        )
        
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=os.getenv('SHOUTBOX_TO'),
            subject="Test Email with Attachment via Flask",
            html="<h1>Test</h1><p>This email includes an attachment.</p>",
            attachments=[attachment]
        )
        
        response = shoutbox.send(email)
        return jsonify({'success': True, 'response': response})
    
    # Test endpoint
    response = client.post('/send-with-attachment')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_bulk_email_endpoint(app, client):
    """Test bulk email sending"""
    shoutbox = ShoutboxClient()
    
    @app.route('/send-bulk', methods=['POST'])
    def send_bulk():
        # Split SHOUTBOX_TO into multiple recipients if it contains commas
        to_addresses = [addr.strip() for addr in os.getenv('SHOUTBOX_TO').split(',')]
        
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=to_addresses,
            subject="Test Bulk Email via Flask",
            html="<h1>Test</h1><p>This is a bulk test email.</p>"
        )
        
        response = shoutbox.send(email)
        return jsonify({'success': True, 'response': response})
    
    # Test endpoint
    response = client.post('/send-bulk')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_error_handling(app, client):
    """Test error handling in Flask integration"""
    shoutbox = ShoutboxClient()
    
    @app.route('/send-error', methods=['POST'])
    def send_error():
        try:
            # Try to send with invalid email
            email = Email(
                from_email="invalid-email",  # Invalid email to trigger error
                to=os.getenv('SHOUTBOX_TO'),
                subject="Test Error Handling",
                html="<h1>Test</h1>"
            )
            
            response = shoutbox.send(email)
            return jsonify({'success': True, 'response': response})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    # Test endpoint
    response = client.post('/send-error')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data
