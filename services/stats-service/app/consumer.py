import pika
import json
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")


def callback(ch, method, properties, body):
    print("EVENT:", json.loads(body))


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
    auto_ack=True,
)

print("Consumer started")
channel.start_consuming()