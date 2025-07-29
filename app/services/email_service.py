from flask_mail import Message
from flask import current_app
from app.email_extension import mail


def send_verification_email(to_email, verification_code):
    subject = "Verify your email"
    sender = "hello@mcurduman.app"

    # Plain text fallback
    body = f"""
    Hey,

    You're receiving this email to verify your address.
    Your verification code is: {verification_code}

    If you did not request this, please ignore this email.
    """

    msg = Message(subject=subject, recipients=[to_email], sender=sender)
    msg.body = body

    msg = Message(subject=subject, recipients=[to_email], sender=sender)
    msg.body = body

    try:
        mail.send(msg)
        return True, "Email sent successfully"
    except Exception as e:
        current_app.logger.error(f"Email send failed: {e}")
        return False, str(e)
