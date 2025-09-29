import smtplib
from email.mime.text import MIMEText
from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
from app.utils.logger import get_logger

logger = get_logger(__name__)


def handle_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())

        logger.info(f"Email successfully sent to {to_email} with subject '{subject}'")
        return f"Email successfully sent to {to_email}"
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return f"Failed to send email: {str(e)}"
