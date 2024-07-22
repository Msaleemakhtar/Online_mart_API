# Notification Management MicroService

## Overview
The notification Service allows you to manage notifications of users and order services .


## Technologies
- **FastAPI**: For API development.
- **PostgreSQL**: For data storage.
- **Kafka**: For event streaming.
- **Protobuf**: For data serialization.
- **Docker**: For containerization.
- **Kong**: For API Gateway management.


## Environment Variables
- `DATABASE_URL`: Connection URL for PostgreSQL.
- `BOOTSTRAP_SERVER`: Kafka broker URL used for connecting to the Kafka cluster.
- `KAFKA_USER_TOPIC`: Kafka topic used for publishing and subscribing to user-related events
- `KAFKA_ORDER_TOPIC`: Kafka topic used for publishing and subscribing to order-related events.
- `KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION`: Kafka consumer group to receive the event from Kafka. 


## Running the Service
run the docker compose and hit the url http://localhost:8000/notification-service/docs in browser to access the endpoints
```sh
docker compose up --build 
```

# Gmail API Email Sender

This Python script demonstrates how to use the Gmail API to send emails using OAuth 2.0 for authentication. The script relies on Google’s API client libraries and requires setup with credentials and token files to function correctly.

## Requirements

- Python 3.x
- Google API client libraries
- OAuth 2.0 credentials from Google Cloud Console

## Setup

**Install Dependencies:**

   Ensure you have the required Python packages installed. You can install them using:

   ```bash
   poetry add google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Setting Up Gmail API Credentials

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
   - Move the downloaded `credentials.json` file to the `/code/app/` directory of your project.

Make sure to keep your `credentials.json` file secure and do not expose it publicly.



# Running the Script

When you run the script for the first time, it will prompt you to authorize access to your Google account. This process will generate a `token.json` file in the `/code/app/` directory, which will be used for future authentication.

## Run the Script

Execute the script using the following command:

```bash
python script_name.py
