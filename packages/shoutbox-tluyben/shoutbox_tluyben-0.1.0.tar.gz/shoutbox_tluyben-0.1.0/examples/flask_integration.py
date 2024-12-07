"""
Example of Flask integration with Shoutbox
"""

import os
from flask import Flask, request, jsonify
from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment

app = Flask(__name__)

# Initialize Shoutbox client
client = ShoutboxClient(api_key=os.getenv('SHOUTBOX_API_KEY'))

@app.route('/send-email', methods=['POST'])
def send_email():
    """Basic email sending endpoint"""
    try:
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=request.json.get('to', os.getenv('SHOUTBOX_TO')),
            subject=request.json['subject'],
            html=request.json['html']
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/send-email-with-attachment', methods=['POST'])
def send_email_with_attachment():
    """Email sending endpoint with file attachment support"""
    try:
        # Get file from request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
            
        file = request.files['file']
        
        # Create attachment
        attachment = Attachment(
            filename=file.filename,
            content=file.read(),
            content_type=file.content_type
        )
        
        # Create email with attachment
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=request.form.get('to', os.getenv('SHOUTBOX_TO')),
            subject=request.form['subject'],
            html=request.form['html'],
            attachments=[attachment]
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/send-bulk-email', methods=['POST'])
def send_bulk_email():
    """Endpoint for sending emails to multiple recipients"""
    try:
        # Use provided recipients or split SHOUTBOX_TO
        to_addresses = request.json.get('to', os.getenv('SHOUTBOX_TO').split(','))
        
        email = Email(
            from_email=os.getenv('SHOUTBOX_FROM'),
            to=to_addresses,
            subject=request.json['subject'],
            html=request.json['html'],
            headers=request.json.get('headers', {})
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/contact-form', methods=['POST'])
def handle_contact_form():
    """Handle contact form submission"""
    try:
        # Create email from form data
        email = Email(
            from_email=EmailAddress(
                request.form['email'],
                request.form.get('name', '')
            ),
            to=os.getenv('SHOUTBOX_FROM'),  # Send to SHOUTBOX_FROM as contact email
            subject=f"Contact Form: {request.form['subject']}",
            html=f"""
                <h2>Contact Form Submission</h2>
                <p><strong>From:</strong> {request.form.get('name', 'Not provided')} ({request.form['email']})</p>
                <p><strong>Subject:</strong> {request.form['subject']}</p>
                <p><strong>Message:</strong></p>
                <p>{request.form['message']}</p>
            """
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'message': 'Thank you for your message!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # For testing purposes
    app.run(debug=True, port=5001)

"""
Example usage with curl:

# Basic email
curl -X POST http://localhost:5001/send-email \
    -H "Content-Type: application/json" \
    -d '{
        "subject": "Test Email",
        "html": "<h1>Hello!</h1><p>This is a test email.</p>"
    }'

# Email with attachment
curl -X POST http://localhost:5001/send-email-with-attachment \
    -F "subject=Test Email with Attachment" \
    -F "html=<h1>Hello!</h1><p>This email has an attachment.</p>" \
    -F "file=@/path/to/file.pdf"

# Bulk email
curl -X POST http://localhost:5001/send-bulk-email \
    -H "Content-Type: application/json" \
    -d '{
        "subject": "Bulk Test Email",
        "html": "<h1>Hello!</h1><p>This is a bulk test email.</p>"
    }'

# Contact form
curl -X POST http://localhost:5001/contact-form \
    -F "name=John Doe" \
    -F "email=john@example.com" \
    -F "subject=Test Contact" \
    -F "message=This is a test contact form submission."
"""
