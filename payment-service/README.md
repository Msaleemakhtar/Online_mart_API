# Payment Management MicroService

## Overview
The Payment Service allows you to manage order payments.


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
run the docker compose and hit the url http://localhost:8000/payment-service/docs in browser to access the endpoints
```sh
docker compose up --build 
```


## Webhook events testing locally
Use Stripe CLI to simulate Stripe events in your local environment:
1. Download the latest linux tar.gz file from Github https://github.com/stripe/stripe-cli/releases/tag/v1.21.0
2. Unzip the file: tar -xvf stripe_X.X.X_linux_x86_64.tar.gz
3. Move ./stripe to your execution path.
4. log in with your Stripe account ./stripe login.
5. run  ./stripe listen --forward-to localhost:8011/webhook


## Navigate through Kong API Gateway to access the API endpoints 
Hit the url http://localhost:8000/payment-service/docs in browser to access the endpoints
1. Use /checkout end point to proceed the order payment and after successful completion will Forward events to your webhook.
