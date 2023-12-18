# RabbitMQ Dockerfile
FROM rabbitmq:latest

COPY rabbitmq.conf /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672
