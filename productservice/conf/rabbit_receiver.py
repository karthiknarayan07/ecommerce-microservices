import pika
from django.conf import settings
import json

def product_queue_receiver():
    credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST,port=settings.RABBIT_PORT, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='product_queue', durable=True)
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
            print(" [x] Received %r" % data)
            
            # case statements for different identifiers for diiferent functionalities
            if data["identifier"] == '1':
                pass
            else:
                print("invalid identifier")
            
            # acknowledge the message to delete from queue
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print("Exception occurred in Rabbit MQ ")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='product_queue', on_message_callback=callback)
    channel.start_consuming()


