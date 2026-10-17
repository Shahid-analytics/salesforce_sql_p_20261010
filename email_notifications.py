
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_failure_email(subject: str, body: str) -> None:
    """
    Send a failure notification email using Gmail SMTP.

    Supports multiple recipients configured in .env.
    """

    sender = os.getenv("GMAIL_SENDER", "").strip()
    app_password = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")
    recipients = [
        email.strip()
        for email in os.getenv("GMAIL_RECIPIENT", "").split(",")
        if email.strip()
    ]

    # Validate configuration
    if not sender:
        raise ValueError("GMAIL_SENDER is missing in .env")

    if not app_password:
        raise ValueError("GMAIL_APP_PASSWORD is missing in .env")

    if not recipients:
        raise ValueError("GMAIL_RECIPIENT is missing in .env")

    # Build email
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.set_content(body)

    # Send email through Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(sender, app_password)
        smtp.send_message(message, to_addrs=recipients)

    print(
        f"Failure notification email sent successfully "
        f"to {len(recipients)} recipient(s)."
    )
