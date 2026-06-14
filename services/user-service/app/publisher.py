import pika
import json
import os
from datetime import datetime, UTC

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")


def publish_user_created(user_id: int, email: str):

    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.queue_declare(
        queue="user_events",
        durable=True
    )

    event = {
        "event": "user_created",
        "user_id": user_id,
        "email": email,
        "created_at": datetime.now(UTC).isoformat(),
    }

    channel.basic_publish(
        exchange="",
        routing_key="user_events",
        body=json.dumps(event),
    )

    connection.close()