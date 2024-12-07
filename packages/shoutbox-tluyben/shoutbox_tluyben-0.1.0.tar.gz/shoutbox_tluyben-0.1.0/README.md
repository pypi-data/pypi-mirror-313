# Shoutbox.net Developer API - Python Library

Shoutbox.net is a Developer API designed to send transactional emails at scale. This documentation covers all Python integration methods, from direct API calls to full framework integration.

## Integration Methods

There are four main ways to integrate with Shoutbox in Python:

1. Direct API calls (minimal dependencies)
2. Using our Python library with pip
3. SMTP integration
4. Web framework integration (Flask/Django)

## 1. Direct API Integration (Minimal Dependencies)

If you want minimal dependencies, you can make direct API calls using `requests`:

```python
import requests

# Your API key from Shoutbox.net
api_key = 'your-api-key-here'

# Prepare email data
data = {
    'from': 'sender@example.com',
    'to': 'recipient@example.com',
    'subject': 'Test Email',
    'html': '<h1>Hello!</h1><p>This is a test email.</p>',
    'name': 'Sender Name',
    'reply_to': 'reply@example.com'
}

# Make the API call
response = requests.post(
    'https://api.shoutbox.net/send',
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    json=data
)

# Handle the response
if response.status_code >= 200 and response.status_code < 300:
    print("Email sent successfully!")
else:
    print(f"Failed to send email. Status code: {response.status_code}")
```

### Direct API Features
- Minimal dependencies (only requests)
- Simple implementation
- Full control over the request
- Lightweight integration
- Suitable for simple implementations

## 2. Python Library with pip

### Installation

```bash
pip install shoutbox
```

### 2.1 API Client Usage

The API client provides an object-oriented interface to the REST API:

```python
from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment

# Initialize client
api_key = os.getenv('SHOUTBOX_API_KEY') or 'your-api-key-here'
client = ShoutboxClient(api_key)

try:
    # Basic email
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Hello!</h1><p>This is a test email.</p>",
        reply_to="reply@example.com"
    )

    client.send(email)
    
    # Email with attachment
    with open('document.pdf', 'rb') as f:
        attachment = Attachment(
            filename='document.pdf',
            content=f.read(),
            content_type='application/pdf'
        )

    email_with_attachment = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email with Attachment",
        html="<h1>Hello!</h1><p>This email includes an attachment.</p>",
        attachments=[attachment]
    )

    client.send(email_with_attachment)

except Exception as e:
    print(f"Error: {str(e)}")
```

### 2.2 SMTP Client Usage

The SMTP client provides an alternative way to send emails:

```python
from shoutbox import SMTPClient, Email

client = SMTPClient('your-api-key-here')

try:
    # Multiple recipients
    email = Email(
        from_email="sender@example.com",
        to=["recipient1@example.com", "recipient2@example.com"],
        subject="Test Email",
        html="<h1>Hello!</h1><p>This is a test email.</p>",
        headers={
            'X-Custom-Header': 'Custom Value',
            'X-Priority': '1'
        }
    )

    client.send(email)

except Exception as e:
    print(f"Error: {str(e)}")
```

### Library Features
- Type-safe email options
- Built-in error handling
- File attachment support
- Custom headers support
- Multiple recipient types (to, cc, bcc)
- Choice between API and SMTP clients

## 3. Web Framework Integration

### Flask Integration

```python
from flask import Flask
from shoutbox import ShoutboxClient, Email

app = Flask(__name__)
client = ShoutboxClient(api_key='your-api-key')

@app.route('/send-email', methods=['POST'])
def send_email():
    email = Email(
        from_email="your-app@domain.com",
        to=request.json['to'],
        subject=request.json['subject'],
        html=request.json['html']
    )
    
    result = client.send(email)
    return {'success': True}
```

### Django Integration

1. Add configuration to `settings.py`:
```python
SHOUTBOX_API_KEY = 'your-api-key'
```

2. Usage example:
```python
from shoutbox import ShoutboxClient, Email

client = ShoutboxClient()

def send_notification(request):
    email = Email(
        from_email="your-app@domain.com",
        to="recipient@example.com",
        subject="Notification",
        html="<h1>New notification</h1>"
    )
    
    client.send(email)
    return JsonResponse({'success': True})
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/shoutboxnet/shoutbox-python.git
```

2. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
make test
```

## Support

- GitHub Issues for bug reports
- Email support for critical issues
- Documentation for guides and examples
- Regular updates and maintenance

## License

This library is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
