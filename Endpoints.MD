
## End Points

Hosted IP:- http://20.40.54.159

Prometheus Metrics:- http://20.40.54.159:8045/targets

RabbitMQ Management:- http://20.40.54.159:8031/

Super Admin login:- [ `8096675401`, `password`]

Enduser login:- [ `8096675402`, `password`]

All Services Login:- [ `karthik`, `password`]

### User service:
* Register Enduser
* Register SuperAdmin
* Login
* Internal (S2S) - Get user data
* Prometheus Metrics - scraping

### Product service
* View products Enduser
* CRUD products SuperAdmin
* Place order
* Prometheus Metrics - scraping

### Order service
* View orders - Enduser
* internal (S2S) - place order
* Prometheus Metrics - scraping

### Communication service
* Prometheus Metrics - scraping