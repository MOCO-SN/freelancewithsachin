import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_booking_email(booking_details):
    msg = MIMEMultipart()

    msg["From"] = os.environ.get("MAIL_FROM", "")
    msg["To"] = os.environ.get("MAIL_TO", "")
    msg["Subject"] = f"New Booking Request from {booking_details['name']}"

    body = f"""
New Booking Request

Name: {booking_details['name']}
Email: {booking_details['email']}
Service: {booking_details['service']}
Preferred Date: {booking_details.get('date', 'Not specified')}

Project Brief:
{booking_details.get('brief', 'Not provided')}
"""

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(
            os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
            int(os.environ.get("MAIL_PORT", 587)),
        )

        server.starttls()

        server.login(
            os.environ.get("MAIL_USERNAME", ""),
            os.environ.get("MAIL_PASSWORD", ""),
        )

        server.sendmail(
            os.environ.get("MAIL_FROM", ""),
            os.environ.get("MAIL_TO", ""),
            msg.as_string(),
        )

        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        print("Email Error:", e)