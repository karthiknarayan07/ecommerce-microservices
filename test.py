# # sender.py

# import pika

# def send_message(message):
#     connection_params = pika.ConnectionParameters(
#         host='20.40.54.159',
#         port=8030,
#         credentials=pika.PlainCredentials(
#             username='karthik',
#             password='password'
#         )
#     )

#     connection = pika.BlockingConnection(connection_params)
#     channel = connection.channel()

#     channel.queue_declare(queue='user_queue')
#     channel.basic_publish(exchange='', routing_key='user_queue', body=message)

#     print(f" [x] Sent '{message}'")

#     connection.close()

# # Example usage
# send_message('Hello RabbitMQ!')
