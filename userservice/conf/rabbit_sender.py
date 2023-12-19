import pika
import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

# using singleton pattern to create a single connection object results in better performance in case of multiple requests (concurrent)) 
# and also prevents the creation of multiple connections to the rabbitmq server

class RabbitSingleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RabbitSingleton, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def __init__(self):
        if not self.connection:
            credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=settings.RABBIT_HOST, port=settings.RABBIT_PORT, credentials=credentials))
            self.channel = self.connection.channel()

    def send_message(self, message, queue):
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message, cls=DjangoJSONEncoder),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )