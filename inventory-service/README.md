# Inventory Management MicroService

## Overview
The Inventory Service manages and receives inventory related event from kafaka and performs crud operations to manage the inventory.


## Technologies
- **FastAPI**: For API development.
- **PostgreSQL**: For data storage.
- **Kafka**: For event streaming.
- **Protobuf**: For data serialization.
- **Docker**: For containerization.
- **Kong**: For API Gateway management.

## Endpoints
![Endpoints](/public/inventory.png)

## Environment Variables
- `DATABASE_URL`: Connection URL for PostgreSQL.
- `BOOTSTRAP_SERVER`: Kafka broker URL used for connecting to the Kafka cluster.
- `KAFKA_PRODUCT_TOPIC`: Kafka topic used for publishing and subscribing to product-related events.
- `KAFKA_INVENTORY_TOPIC`: Kafka topic used for publishing and subscribing to product-related events.
- `KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY`: Kafka consumer group to receive the event from Kafka. 




## Running the Service
run the docker compose and hit the url http://localhost:8000/inventory-service/docs in browser to access the complete api

```sh
docker compose up --build
