import json
import os
from datetime import datetime

import pika

from app.db.database import SessionLocal
from app.db.models import UserEvent


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")


def callback(ch, method, properties, body):
    event = json.loads(body)
    print("Received:", event)

    db = SessionLocal()
    

    try:
        user_event = UserEvent(
            user_id=event["user_id"],
            email=event["email"],
            event_type=event["event"],
            created_at=datetime.fromisoformat(
                event["created_at"]
            ),
        )

        db.add(user_event)
        db.commit()

        print("Saved event:", event)

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


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

channel.basic_consume(
    queue="user_events",
    on_message_callback=callback,
    auto_ack=False,
)

print("Consumer started")

channel.start_consuming()