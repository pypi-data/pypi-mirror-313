import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


class PostmarkEmailSender:
    SMTP_SERVER = "smtp.postmarkapp.com"
    SMTP_PORT = 587

    def __init__(self):
        load_dotenv()
        api_token = os.getenv("POSTMARK_API_TOKEN")
        sender_email = os.getenv("SENDER_EMAIL")
        if api_token is None:
            raise ValueError("POSTMARK_API_TOKEN not found in environment variables")
        self.api_token = api_token
        if sender_email is None:
            raise ValueError("SENDER_EMAIL not found in environment variables")
        self.sender_email = sender_email

    def send_email(self, to_email: str, subject: str, body: str):
        """Send an email using Postmark SMTP server."""
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()  # Enable TLS
                server.login(
                    self.api_token, self.api_token
                )  # Using API token as both username and password
                server.send_message(msg)
                return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
