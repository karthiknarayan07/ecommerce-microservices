import pika
from django.conf import settings
import json

def user_queue_receiver():
    credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='user_queue', durable=True)
    print("*************************************")
    print("*************************************")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    print("*************************************")
    print("*************************************")

    def callback(ch, method, properties, body):
        try:
            if type(body) == bytes:
                body = body.decode()
            body = body.replace("\'", "\"")
            data = json.loads(body)
            try:
                if data["identifier"] == 1:
                    pass
                else:
                    print("invalid identifier")
            except Exception as error:
                pass
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Exception occurred in Rabbit MQ ")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='user_queue', on_message_callback=callback)
    channel.start_consuming()


