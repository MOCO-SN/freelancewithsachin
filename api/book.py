import json
import os
import urllib.parse

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from message_helper import get_text_message_input, send_message
from lib.email_helper import send_booking_email


def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"}),
        }

    try:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        form = urllib.parse.parse_qs(body)
    except Exception:
        form = {}

    name = form.get("name", [""])[0]
    email = form.get("email", [""])[0]
    service = form.get("service", [""])[0]
    date = form.get("date", [""])[0]
    brief = form.get("brief", [""])[0]

    if not name or not email or not service:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": "Missing required fields"
            }),
        }

    try:
        whatsapp_msg = f"""Booking Request

Name: {name}
Email: {email}
Service: {service}
Preferred Date: {date or 'Not specified'}

Brief:
{brief or 'Not provided'}
"""

        data = get_text_message_input(
            os.environ.get("RECIPIENT_WAID", ""),
            whatsapp_msg,
        )

        send_message(data)

        print("WhatsApp message sent.")

    except Exception as e:
        print("WhatsApp Error:", e)

    try:
        send_booking_email({
            "name": name,
            "email": email,
            "service": service,
            "date": date,
            "brief": brief,
        })

    except Exception as e:
        print("Email Error:", e)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"status": "success"}),
    }