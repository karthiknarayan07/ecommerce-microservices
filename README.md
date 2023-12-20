## Tech Stack

**Backend:** Python, Django, DRF

**Infra:** Docker-compose

**Database:** PostgreSQL

**Others:** Redis, RabbitMQ, Prometheus, NGINX

## Deployment

Clone the project

```bash
  git clone https://github.com/karthiknarayan07/ecommerce-microservices.git
```

Go to the project directory

```bash
  cd ecommerce-microservices
```

Go to databases folder

```bash
  cd databases
```

build docker images

```bash
  docker compose build
```

Start all databases

```bash
  docker compose up
```

Go to parent folder to build services

```bash
  cd ..
```

build docker images

```bash
  docker compose build
```

Start all services

```bash
  docker compose up
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`NGINX_PORT`

`PROMETHEUS_PORT`

`RABBITMQ_PORT`
`RABBITMQ_MANAGEMENT_PORT`

`REDIS_PORT`
`REDIS_PASSWORD`

`USERSERVICE_CONTAINER_PORT_1`
`USERSERVICE_CONTAINER_PORT_2`

`PRODUCTSERVICE_CONTAINER_PORT_1`
`PRODUCTSERVICE_CONTAINER_PORT_2`

`ORDERSERVICE_CONTAINER_PORT_1`
`ORDERSERVICE_CONTAINER_PORT_2`

`COMMUNICATIONSERVICE_CONTAINER_PORT_1`
`COMMUNICATIONSERVICE_CONTAINER_PORT_2`

## Authors

- [@Karthik Narayan](https://www.github.com/karthiknarayan07)
