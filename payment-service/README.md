# Payment Management MicroService

## Overview
The Order Service manages and receives inventory, user and product related events from kafaka and performs crud operations to manage the orders.


## Technologies
- **FastAPI**: For API development.
- **PostgreSQL**: For data storage.
- **Kafka**: For event streaming.
- **Protobuf**: For data serialization.
- **Docker**: For containerization.
- **Kong**: For API Gateway management.

## Endpoints
![Endpoints](/public/payment.png)

## Environment Variables
- `DATABASE_URL`: Connection URL for PostgreSQL.
- `BOOTSTRAP_SERVER`: Kafka broker URL used for connecting to the Kafka cluster.
- `KAFKA_USER_TOPIC`: Kafka topic used for publishing and subscribing to user-related events
- `KAFKA_ORDER_TOPIC`: Kafka topic used for publishing and subscribing to order-related events.
- `KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT`: Kafka consumer group to receive the event from Kafka. 
- `STRIPE_SECRET_KEY`: .
- `TRIPE_WEBHOOK_SECRET`: .




## Running the Service
run the docker compose and hit the url http://localhost:8000/order-service/docs in browser to access the complete api

```sh
docker compose up --build
