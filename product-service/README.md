# Product Management MicroService

## Overview
The Product Service manages product crud operations, review and rating of product and send to kafka for event streaming.



## Technologies
- **FastAPI**: For API development.
- **PostgreSQL**: For data storage.
- **Kafka**: For event streaming.
- **Protobuf**: For data serialization.
- **Docker**: For containerization.
- **Kong**: For API Gateway management.

## Endpoints
![Endpoints](/public/product.png)

## Environment Variables
- `DATABASE_URL`: Connection URL for PostgreSQL.
- `BOOTSTRAP_SERVER`: Kafka broker URL used for connecting to the Kafka cluster.
- `KAFKA_PRODUCT_TOPIC`: Kafka topic used for publishing and subscribing to product-related events.




## Running the Service
run the docker compose and hit the url http://localhost:8000/product-service/docs in browser 

```sh
docker compose up --build
