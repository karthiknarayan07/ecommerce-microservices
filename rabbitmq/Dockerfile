# RabbitMQ Dockerfile
FROM rabbitmq:latest

RUN rabbitmq-plugins enable --offline rabbitmq_management

COPY rabbitmq.conf /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672 15672