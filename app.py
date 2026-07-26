"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
"""

import json


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