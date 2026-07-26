"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
"""

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request, jsonify
import flask

from message_helper import get_text_message_input, send_message

app = Flask(__name__)

app.config["ACCESS_TOKEN"] = os.environ.get("ACCESS_TOKEN", "")
app.config["PHONE_NUMBER_ID"] = os.environ.get("PHONE_NUMBER_ID", "")
app.config["VERSION"] = os.environ.get("VERSION", "v18.0")
app.config["RECIPIENT_WAID"] = os.environ.get("RECIPIENT_WAID", "")
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
app.config["MAIL_FROM"] = os.environ.get("MAIL_FROM", "")
app.config["MAIL_TO"] = os.environ.get("MAIL_TO", "")


def get_services():
    return [
        {
            "id": 1,
            "title": "Website Development",
            "service_key": "Website",
            "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWPhvJRKcvT0V4hYgZnnMlBjbpTBFaKjYHl9vbAzXz_g&s=10",
            "document": "https://github.com/fbsamples/whatsapp-api-examples/blob/main/send-messages-flight-app-python/FlightConfirmation.pdf",
            "category": "Web Dev",
            "description": "Full-stack responsive websites with custom designs and modern frameworks",
            "price": "Depends on project",
            "duration": "1-2 weeks",
        },
        {
            "id": 2,
            "title": "App Development",
            "service_key": "App",
            "thumbnail": "https://hidigital.hd.cw.vuurrood.dev/app/uploads/sites/2/HD_Logo_Appstore-Playstore-1000x1000-d5b77b2a305d2b4f58dbd2266868d38f.png",
            "document": "https://github.com/fbsamples/whatsapp-api-examples/blob/main/send-messages-flight-app-python/FlightConfirmation.pdf",
            "category": "App Dev",
            "description": "Cross-platform apps built with React Native and Flutter",
            "price": "Depends on project",
            "duration": "2-4 weeks",
        },
        {
            "id": 3,
            "title": "Video Editing",
            "service_key": "Video editor",
            "thumbnail": "https://assets-static.invideo.io/images/large/Simplified_Editor_UI_1_fb9de2b9c0.webp",
            "document": "https://github.com/fbsamples/whatsapp-api-examples/blob/main/send-messages-flight-app-python/FlightConfirmation.pdf",
            "category": "Video",
            "description": "Editing, motion graphics, color grading for reels and commercials",
            "price": "Depends on project",
            "duration": "3-5 days",
        },
    ]


@app.route("/")
def index():
    return render_template(
        "index.html",
        services=get_services(),
        name=__name__,
    )


@app.route("/welcome", methods=["POST"])
def welcome():
    try:
        data = get_text_message_input(
            app.config["RECIPIENT_WAID"],
            "Welcome to the Mocosn Freelance Service Booking Demo!",
        )

        send_message(data)

    except Exception as e:
        print("WhatsApp Error:", e)

    return flask.redirect(flask.url_for("index"))


def send_booking_email(booking_details):
    msg = MIMEMultipart()

    msg["From"] = app.config["MAIL_FROM"]
    msg["To"] = app.config["MAIL_TO"]
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
            app.config["MAIL_SERVER"],
            app.config["MAIL_PORT"],
        )

        server.starttls()

        server.login(
            app.config["MAIL_USERNAME"],
            app.config["MAIL_PASSWORD"],
        )

        server.sendmail(
            app.config["MAIL_FROM"],
            app.config["MAIL_TO"],
            msg.as_string(),
        )

        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        print("Email Error:", e)


@app.route("/book", methods=["POST"])
def book_service():

    name = request.form.get("name")
    email = request.form.get("email")
    service = request.form.get("service")
    date = request.form.get("date")
    brief = request.form.get("brief")

    if not name or not email or not service:
        return jsonify({
            "status": "error",
            "message": "Missing required fields"
        }), 400

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
            app.config["RECIPIENT_WAID"],
            whatsapp_msg,
        )

        send_message(data)

        print("WhatsApp message sent.")

    except Exception as e:
        print("WhatsApp Error:", e)

    send_booking_email({
        "name": name,
        "email": email,
        "service": service,
        "date": date,
        "brief": brief,
    })

    return jsonify({
        "status": "success"
    })


# if __name__ == "__main__":
#     app.run(debug=True)