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

    # HTML version
    html = f"""
    <div style="font-family:Segoe UI, sans-serif; max-width:500px; padding:1rem; border-radius:10px; background:#f9f9f9;">
      <h2 style="color:#212121;">Email Verification</h2>
      <p>Hello,</p>
      <p>Your verification code is:</p>
      <div style="font-size:1.5rem; font-weight:bold; padding:0.5rem 1rem; background:#e0f7fa; display:inline-block; border-radius:8px; margin:1rem 0;">
        {verification_code}
      </div>
      <p>This code is valid for 15 minutes. If you did not request this, you can safely ignore it.</p>
      <p style="margin-top:2rem;">Thanks,<br><strong>Your App Team</strong></p>
    </div>
    """

    msg = Message(subject=subject, recipients=[to_email], sender=sender)
    msg.body = body
    msg.html = html

    msg = Message(subject=subject, recipients=[to_email],sender=sender)
    msg.body = body

    try:
        mail.send(msg)
        return True, "Email sent successfully"
    except Exception as e:
        current_app.logger.error(f"Email send failed: {e}")
        return False, str(e)
