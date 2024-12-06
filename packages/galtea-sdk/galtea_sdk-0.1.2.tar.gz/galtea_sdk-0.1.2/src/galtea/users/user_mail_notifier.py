from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
import os,random, string
import argilla as rg
from galtea.utils import sanitize_string
from galtea.users.html_email_template import HTML_EMAIL_TEMPLATE


class UserEmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_port = int(os.getenv("SMTP_PORT", default=465))
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("SMTP_SENDER_EMAIL")

    def parse_username_from_email(self, email: str) -> str:
        return sanitize_string(email.split("@")[0])

    def send_mail(self, receiver: str, message: str):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.sender_email, receiver, message)
                print(f"Email sent to {receiver}")
        except smtplib.SMTPServerDisconnected as e:
            print(f"Could not connect to SMTP server, please check your credentials")
            return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
        return True

    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def send_user_credentials_email(self, first_name: str, last_name: str, email: str, username: str, password: str, workspace: rg.Workspace, argilla_url: str = os.getenv("ARGILLA_API_URL")):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Argilla annotation tool credentials"
        message["From"] = self.sender_email
        message["To"] = email

        template = HTML_EMAIL_TEMPLATE.substitute({
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "workspace": workspace.name,
            "argilla_url": argilla_url
        })

        part = MIMEText(template, "html")
        message.attach(part)

        return self.send_mail(email, message.as_string())

    def send_user_credentials(self, credentials: dict) -> bool:
        print(f"Sending credentials to email {credentials['email']}, username: {credentials['username']}")   
        return self.send_user_credentials_email(credentials['first_name'], credentials['last_name'], credentials['email'], credentials['username'], credentials['password'], credentials['workspace'])
   

#