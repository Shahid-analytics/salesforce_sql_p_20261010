
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("GMAIL_SENDER")
app_password = os.getenv("GMAIL_APP_PASSWORD")
recipient = os.getenv("GMAIL_RECIPIENT")

if not all([sender, app_password, recipient]):
    raise ValueError("Missing Gmail settings in .env")

message = EmailMessage()
message["Subject"] = "Prefect Email Test"
message["From"] = sender
message["To"] = recipient
message.set_content(
    "Success! Gmail email notifications are working. "
    "This is a test for the Salesforce Prefect pipeline."
)

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(sender, app_password)
    smtp.send_message(message)

print("Test email sent successfully.")
