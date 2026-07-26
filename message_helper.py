"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
"""

import json
import os
import requests


def _get_config(key):
    return os.environ.get(key, "")


def send_message(data):
    access_token = _get_config("ACCESS_TOKEN")
    phone_number_id = _get_config("PHONE_NUMBER_ID")
    version = _get_config("VERSION", "v18.0")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    url = (
        f"https://graph.facebook.com/"
        f"{version}/"
        f"{phone_number_id}/messages"
    )

    try:
        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=30,
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        return response

    except requests.exceptions.RequestException as e:
        print("WhatsApp API Error:", e)
        return None


def get_text_message_input(recipient, text):
    return json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    })


def get_templated_message_input(recipient, service):
    return json.dumps({
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": "sample_service_booking",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "filename": "ServiceProposal.pdf",
                                "link": service["document"]
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": service["category"]
                        },
                        {
                            "type": "text",
                            "text": service["description"]
                        },
                        {
                            "type": "text",
                            "text": f"{service['price']} — Est. {service['duration']}"
                        }
                    ]
                }
            ]
        }
    })