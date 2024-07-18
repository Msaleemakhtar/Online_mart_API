# User Management MicroService

## Overview
The User Service manages user authentication, registration, and profiles.



## Technologies
- **FastAPI**: For API development.
- **PostgreSQL**: For data storage.
- **Kafka**: For event streaming.
- **Protobuf**: For data serialization.
- **Docker**: For containerization.
- **Kong**: For API Gateway management.

## Endpoints
![Endpoints](/public/users.png)

## Environment Variables
- `DATABASE_URL`: Connection URL for PostgreSQL.
- `BOOTSTRAP_SERVER`: Kafka broker URL used for connecting to the Kafka cluster.
- `KAFKA_USER_TOPIC`: Kafka topic used for publishing and subscribing to user-related events.
- `SECRET_KEY`:Secret key used for signing and verifying JWT tokens.
- `ALGORITHM`: Algorithm used for JWT token encoding.
- `ACCESS_TOKEN_EXPIRE_MINUTES`:Expiry time for access tokens in minutes.
- `REFRESH_TOKEN_EXPIRE_MINUTES`: Expiry time for refresh tokens in minutes.



## Running the Service
```sh
docker-compose up --build
