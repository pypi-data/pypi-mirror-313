"""
Shoutbox SMTP client
~~~~~~~~~~~~~~~~~

This module contains the SMTP client class.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from .models import Email
from .exceptions import ShoutboxError

class SMTPClient:
    """Client for the Shoutbox SMTP service"""
    
    def __init__(
        self, 
        api_key: str = None,
        host: str = "mail.shoutbox.net",  
        port: int = 587,
        use_tls: bool = True,
        timeout: int = 30
    ):
        self.api_key = api_key or os.getenv('SHOUTBOX_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in SHOUTBOX_API_KEY environment variable")
        
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.timeout = timeout

    def send(self, email: Email) -> bool:
        """
        Send an email using the Shoutbox SMTP service
        
        Args:
            email: Email object containing the email details
            
        Returns:
            bool: True if email was sent successfully
            
        Raises:
            ValidationError: If email validation fails
            ShoutboxError: For SMTP-related errors
        """
        try:
            # Create message container
            msg = MIMEMultipart('alternative')
            msg['Subject'] = email.subject
            
            # Set From header with name if provided
            if email.from_email:
                msg['From'] = str(email.from_email)
            
            # Set To header(s)
            msg['To'] = ', '.join(str(addr) for addr in email.to)
            
            # Set CC header(s) if provided
            if email.cc:
                msg['Cc'] = ', '.join(str(addr) for addr in email.cc)
            
            # Set Reply-To if provided
            if email.reply_to:
                msg['Reply-To'] = str(email.reply_to)
            
            # Add custom headers if any
            if email.headers:
                for key, value in email.headers.items():
                    msg[key] = str(value)
            
            # Attach HTML content
            msg.attach(MIMEText(email.html, 'html'))
            
            # Add attachments if any
            for attachment in email.attachments:
                mime_attachment = MIMEApplication(attachment.content)
                mime_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=attachment.filename
                )
                if attachment.content_type:
                    mime_attachment.add_header(
                        'Content-Type',
                        attachment.content_type
                    )
                msg.attach(mime_attachment)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.api_key, self.api_key)
                
                # Get all recipient addresses
                recipients = [addr.email for addr in email.to]
                if email.cc:
                    recipients.extend(addr.email for addr in email.cc)
                if email.bcc:
                    recipients.extend(addr.email for addr in email.bcc)
                
                # Send the email
                server.send_message(msg, to_addrs=recipients)
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            raise ShoutboxError("SMTP authentication failed")
        except smtplib.SMTPException as e:
            raise ShoutboxError(f"SMTP error: {str(e)}")
        except Exception as e:
            raise ShoutboxError(f"Unexpected error: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # No cleanup needed
