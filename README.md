# 🌟 Online Mart API Using Event-Driven Microservices Architecture

## 📜 Project Overview

Welcome to the **Online Mart API** project! This initiative focuses on developing a comprehensive, scalable, and efficient system for managing an online mart. The project leverages cutting-edge technologies and modern architectural patterns to ensure high performance and reliability.

- **Build a scalable and efficient API** for an online mart using a microservices architecture.
- **Implement an event-driven system** to facilitate asynchronous communication between services.
- **Adopt modern technologies** including FastAPI for API development, Docker for containerization, and Kafka for event streaming.
- **Streamline development and deployment** processes with DevContainers and Docker Compose.
- **Route and manage API requests** through Kong API Gateway for enhanced control and scalability.
- **Employ Protocol Buffers (Protobuf)** to achieve efficient data serialization and communication.
- **Persist data reliably** using PostgreSQL as the primary database system.

## 🎯 Objectives

- **Develop a scalable and efficient API** for an online mart using microservices.
- **Implement an event-driven architecture** to handle asynchronous communication between services.
- **Utilize modern technologies** such as FastAPI for API development, Docker for containerization, and Kafka for event streaming.
- **Ensure smooth development and deployment** using DevContainers and Docker Compose.
- **Manage and route API requests** through Kong API Gateway.
- **Use Protocol Buffers (Protobuf)** for efficient data serialization.
- **Persist data** using PostgreSQL.

## 🛠 Technologies

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Docker**: For containerizing the microservices, ensuring consistency across different environments.
- **DevContainers**: To provide a consistent development environment.
- **Docker Compose**: For orchestrating multi-container Docker applications.
- **PostgreSQL**: A powerful, open-source relational database system.
- **SQLModel**: For interacting with the PostgreSQL database using Python.
- **Kafka**: A distributed event streaming platform for building real-time data pipelines and streaming applications.
- **Protocol Buffers (Protobuf)**: A method developed by Google for serializing structured data, similar to XML or JSON but smaller, faster, and simpler.
- **Kong**: An open-source API Gateway and Microservices Management Layer.

## 🧩 Microservices

1. **User Service**: Manages user authentication, registration, and profiles.
2. **Product Service**: Manages product catalog, including CRUD operations for products.
3. **Order Service**: Handles order creation, updating, and tracking.
4. **Inventory Service**: Manages stock levels and inventory updates.
5. **Notification Service**: Sends notifications (email, SMS) to users about order statuses and other updates.
6. **Payment Service**: Processes payments and manages transaction records.

## 🚀 Event-Driven Communication

- **Kafka**: Acts as the event bus, facilitating communication between microservices. Each service can produce and consume messages (events) such as user registration, order placement, and inventory updates.
- **Protobuf**: Used for defining the structure of messages exchanged between services, ensuring efficient and compact serialization.

## 🗄 Data Storage

- **PostgreSQL**: Each microservice with data persistence needs will have its own PostgreSQL database instance, following the database-per-service pattern.

## 🛡 API Gateway

- **Kong**: Manages API request routing, authentication, rate limiting, and other cross-cutting concerns.

## 💻 Development Environment

- **DevContainers**: Provide consistent development environments using VSCode DevContainers, ensuring that all team members work in identical environments.
- **Docker Compose**: Orchestrates the various microservices and dependencies (PostgreSQL, Kafka, etc.) during development and testing.

## 🏁 Getting Started

To get started with the project, follow the setup instructions.

1. Clone the Project

```bash
git clone https://github.com/Msaleemakhtar/Online_mart_API.git

```
2. Run the command to up all microservices's containers

```bash
docker compose --profile database up --build -d
```
3. Register the services and routes in Kong API Gateway

 ```bash
./register_services.sh

```
4. ### Webhook events testing locally
Use Stripe CLI to simulate Stripe events in your local environment:
   1. Download the latest linux tar.gz file from Github https://github.com/stripe/stripe-cli/releases/tag/v1.21.0
   2. Unzip the file: tar -xvf stripe_X.X.X_linux_x86_64.tar.gz
   3. Move ./stripe to your execution path.
   4. log in with your Stripe account ./stripe login.
   5. run  ./stripe listen --forward-to localhost:8011/webhook


5. ### Setting Up Gmail API Credentials

To use the Gmail API in your project, follow these steps to obtain and configure your OAuth 2.0 credentials:

   1. **Go to the Google Cloud Console:**
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).

   2. **Create a New Project or Select an Existing Project:**
   - Click on the project dropdown in the top navigation bar.
   - Choose `New Project` to create a new one, or select an existing project from the list.

   3. **Enable the Gmail API:**
   - In the left-hand menu, go to `APIs & Services` > `Library`.
   - Search for "Gmail API" and click on it.
   - Click the `Enable` button.

   4. **Create OAuth 2.0 Credentials:**
   - In the left-hand menu, go to `APIs & Services` > `Credentials`.
   - Click on `Create Credentials` and select `OAuth Client ID`.
   - If prompted, configure the OAuth consent screen with necessary details.
   - For `Application type`, select `desktop application`.
   - Set the `Authorized redirect URIs` according to your application's requirements.
   - Click `Create`.

   5. **Download the Credentials:**
   - After creating the OAuth 2.0 Client ID, you will be provided with a `credentials.json` file.
   - Download this file to your local system.

   6. **Place the `credentials.json` File:**
   - Move the downloaded `credentials.json` file to the `/code/app/` directory of your project. Make sure to keep your `credentials.json` file secure and do not expose it publicly.
   7. **Running the Script:**
   When you run the script for the first time, it will prompt you to authorize access to your Google account. This process will generate a `token.json` file in the `/code/app/` directory, which will be used for future authentication.
   Execute the script using the following command:

   ```bash
   python script_name.py
   ```


6. 🌐 Checkout All Microservices in Browser

- 📊 Kafka UI: [http://localhost:8080/](http://localhost:8080/)
- 🛡️ Kong UI: [http://localhost:8002/](http://localhost:8002/)
- 👤 User Microservice: [http://localhost:8000/user-service/docs](http://localhost:8000/user-service/docs)
- 🛍️ Product Microservice: [http://localhost:8000/product-service/docs](http://localhost:8000/product-service/docs)
- 📦 Inventory Microservice: [http://localhost:8000/inventory-service/docs](http://localhost:8000/inventory-service/docs)
- 📜 Order Microservice: [http://localhost:8000/order-service/docs](http://localhost:8000/order-service/docs)
- 💳 Payment Microservice: [http://localhost:8000/payment-service/docs](http://localhost:8000/payment-service/docs)
- ✉️ Notification Microservice: [http://localhost:8000/notification-service/docs](http://localhost:8000/notification-service/docs)

