import pika
import json

RABBITMQ_HOST = "rabbitmq"


def publish_user_created(user_id: int, email: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
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
    }

    channel.basic_publish(
        exchange="",
        routing_key="user_events",
        body=json.dumps(event),
    )

    connection.close()