import pika
import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


def rabbitconnection(message, queue):
    credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message, cls=DjangoJSONEncoder),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()
