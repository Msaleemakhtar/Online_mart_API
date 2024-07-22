
# Online Mart API Using Event-Driven Microservices Architecture

## Project Overview

Welcome to the **Online Mart API** project! This initiative focuses on developing a comprehensive, scalable, and efficient system for managing an online mart. The project leverages cutting-edge technologies and modern architectural patterns to ensure high performance and reliability.

- **Build a scalable and efficient API** for an online mart using a microservices architecture.  
  ![Microservices](https://img.icons8.com/ios/50/000000/microservices.png)

- **Implement an event-driven system** to facilitate asynchronous communication between services.  
  ![Event-Driven Architecture](https://img.icons8.com/ios/50/000000/event-schedule.png)

- **Adopt modern technologies** including FastAPI for API development, Docker for containerization, and Kafka for event streaming.  
  ![FastAPI](https://img.icons8.com/ios/50/ff6600/fastapi.png)  
  ![Docker](https://img.icons8.com/ios/50/2496ed/docker.png)  
  ![Kafka](https://img.icons8.com/ios/50/000000/apache-kafka.png)

- **Streamline development and deployment** processes with DevContainers and Docker Compose.  
  ![DevContainers](https://img.icons8.com/ios/50/000000/visual-studio-code.png)  
  ![Docker Compose](https://img.icons8.com/ios/50/000000/docker-compose.png)

- **Route and manage API requests** through Kong API Gateway for enhanced control and scalability.  
  ![Kong API Gateway](https://img.icons8.com/ios/50/000000/api.png)

- **Employ Protocol Buffers (Protobuf)** to achieve efficient data serialization and communication.  
  ![Protocol Buffers](https://img.icons8.com/ios/50/000000/protobuf.png)

- **Persist data reliably** using PostgreSQL as the primary database system.  
  ![PostgreSQL](https://img.icons8.com/ios/50/336791/postgresql.png)


## Objectives

- **Develop a scalable and efficient API** for an online mart using microservices.
- **Implement an event-driven architecture** to handle asynchronous communication between services.
- **Utilize modern technologies** such as FastAPI for API development, Docker for containerization, and Kafka for event streaming.
- **Ensure smooth development and deployment** using DevContainers and Docker Compose.
- **Manage and route API requests** through Kong API Gateway.
- **Use Protocol Buffers (Protobuf)** for efficient data serialization.
- **Persist data** using PostgreSQL.


## Technologies

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Docker**: For containerizing the microservices, ensuring consistency across different environments.
- **DevContainers**: To provide a consistent development environment.
- **Docker Compose**: For orchestrating multi-container Docker applications.
- **PostgreSQL**: A powerful, open-source relational database system.
- **SQLModel**: For interacting with the PostgreSQL database using Python.
- **Kafka**: A distributed event streaming platform for building real-time data pipelines and streaming applications.
- **Protocol Buffers (Protobuf)**: A method developed by Google for serializing structured data, similar to XML or JSON but smaller, faster, and simpler.
- **Kong**: An open-source API Gateway and Microservices Management Layer.



### Microservices

1. **User Service**: Manages user authentication, registration, and profiles.
2. **Product Service**: Manages product catalog, including CRUD operations for products.
3. **Order Service**: Handles order creation, updating, and tracking.
4. **Inventory Service**: Manages stock levels and inventory updates.
5. **Notification Service**: Sends notifications (email, SMS) to users about order statuses and other updates.
6. **Payment Service**: Processes payments and manages transaction records.


### Event-Driven Communication
- **Kafka**: Acts as the event bus, facilitating communication between microservices. Each service can produce and consume messages (events) such as user registration, order placement, and inventory updates.
- **Protobuf**: Used for defining the structure of messages exchanged between services, ensuring efficient and compact serialization.

### Data Storage

- **PostgreSQL**: Each microservice with data persistence needs will have its own PostgreSQL database instance, following the database-per-service pattern.

### API Gateway

- **Kong**: Manages API request routing, authentication, rate limiting, and other cross-cutting concerns.

## Development Environment

- **DevContainers**: Provide consistent development environments using VSCode DevContainers, ensuring that all team members work in identical environments.
- **Docker Compose**: Orchestrates the various microservices and dependencies (PostgreSQL, Kafka, etc.) during development and testing.




## Getting Started

To get started with the project, follow the [setup instructions](#setup).

