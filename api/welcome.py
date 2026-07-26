import json
import os
import urllib.parse

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from message_helper import get_text_message_input, send_message


def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"}),
        }

    try:
        data = get_text_message_input(
            os.environ.get("RECIPIENT_WAID", ""),
            "Welcome to the Mocosn Freelance Service Booking Demo!",
        )

        send_message(data)

    except Exception as e:
        print("WhatsApp Error:", e)

    return {
        "statusCode": 302,
        "headers": {
            "Location": "/",
        },
        "body": "",
    }