
# Services

API's and services functionality with flow

Each service has `prometheus` metrics implemented

`Note:- Each service has its own PostgreSQL DB and RabbitMQ Queue`
### 1. User Service

* Involves enduser & supedadmins registration and login
* Attached `postman` collection with data for testing
* Product service and order service calls `service-to-service` internal endpoints to get user info using JWT token.
* `RabbitMQ` message is send to communication service to send `signup` email

#### Assumptions

* Assuming only 2 user roles superadmin and enduser
* Later we can implement `API key` or server token security measure for service-to-service communication.
### 2. Product Service

* 3 Endpoints - view products (enduser), CRUD products (superadmin), place order (enduser)
* Implemented cache first pattern, if `cache hit` then read from cache else making DB query and serving, before response the DB data is stored in `redis`
* Only Superadmin can Update and Add products to database
* When new products added or updated `invalidating redis cache`.
* Implemented `pessimistic locking` on products CRUD api.
* Place order API calls `orderservice` by locking product.

#### Assumptions
* We can keep place order api in orderservice also, but DB locking will be from product service so kept it in product service, but functionality is implemented in `orderservice`
### 3. Order service
* 2 Endpoints - View orders(enduser), PlaceOrder(productservice)
* Sends Message to `RabbitMQ` to send order invoice through email.
### 4. Communication Service
* No API endpoints, this is completely async service
* only 2 Functions implemented just to show the architecture.
* `Signup Email sending` - sent from userservice
* `Order Invoice sending` - sent from orderservice
### 5. Prometheus
* One master `Prometheus` container.
* Listens on services mentioned in `Prometheus.yml` configuration file.
* Open server IP with port number mentioned in .env to view the `health` of all services.
* Targets section in Prometheus displays all services.