#!/bin/sh

KONG_ADMIN_URL="http://localhost:8001"

# Wait for Kong to be ready
until $(curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL); do
  printf '.'
  sleep 5
done

# Function to register service and route
register_service() {
  SERVICE_NAME=$1
  SERVICE_URL=$2
  SERVICE_PATH=$3

  # Register Service
  if curl -i -X POST $KONG_ADMIN_URL/services/ \
    --data "name=$SERVICE_NAME" \
    --data "url=$SERVICE_URL"; then
    echo "Registered $SERVICE_NAME successfully."
  else
    echo "Failed to register $SERVICE_NAME."
    exit 1
  fi

  # Register Service Route
  if curl -i -X POST $KONG_ADMIN_URL/services/$SERVICE_NAME/routes \
    --data "paths[]=$SERVICE_PATH" \
    --data "strip_path=true"; then
    echo "Registered route for $SERVICE_NAME successfully."
  else
    echo "Failed to register route for $SERVICE_NAME."
    exit 1
  fi
}

# Register Services
register_service "user-service" "http://host.docker.internal:8006" "/user-service"
register_service "product-service" "http://host.docker.internal:8007" "/product-service"
register_service "inventory-service" "http://host.docker.internal:8008" "/inventory-service"
register_service "order-service" "http://host.docker.internal:8009" "/order-service"
register_service "notification-service" "http://host.docker.internal:8010" "/notification-service"
register_service "payment-service" "http://host.docker.internal:8011" "/payment-service"

echo "All services registered successfully!"








#Alternate Method
# KONG_ADMIN_URL="http://localhost:8001"

# # Wait for Kong to be ready
# until $(curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL); do
#   printf '.'
#   sleep 5
# done



# # Register User Service
# curl -i -X POST $KONG_ADMIN_URL/services/ \
#   --data "name=user-service" \
#   --data "url=http://host.docker.internal:8006"
# # Register User Service routes
# curl -i -X POST $KONG_ADMIN_URL/services/user-service/routes \
#   --data "paths[]=/user-service" \
#   --data "strip_path=true"


# # # Register Product Service
# curl -i -X POST $KONG_ADMIN_URL/services/ \
#   --data "name=product-service" \
#   --data "url=http://host.docker.internal:8007"
# # Register Product Service routes
# curl -i -X POST $KONG_ADMIN_URL/services/product-service/routes \
#   --data "paths[]=/product-service" \
#   --data "strip_path=true"


# # # Register Inventory Service
# curl -i -X POST $KONG_ADMIN_URL/services/ \
#   --data "name=inventory-service" \
#   --data "url=http://host.docker.internal:8008"
# # Register Inventory Service routes
# curl -i -X POST $KONG_ADMIN_URL/services/inventory-service/routes \
#   --data "paths[]=/inventory-service" \
#   --data "strip_path=true"


# # # Register Order Service
# curl -i -X POST $KONG_ADMIN_URL/services/ \
#   --data "name=order-service" \
#   --data "url=http://host.docker.internal:8009"
# # Register Order Service routes
# curl -i -X POST $KONG_ADMIN_URL/services/order-service/routes \
#   --data "paths[]=/order-service" \
#   --data "strip_path=true"


# # # Register Notification Service
# curl -i -X POST $KONG_ADMIN_URL/services/ \
#   --data "name=notification-service" \
#   --data "url=http://host.docker.internal:8010"
# # Register Notification Service routes
# curl -i -X POST $KONG_ADMIN_URL/services/notification-service/routes \
#   --data "paths[]=/notification-service" \
#   --data "strip_path=true"


# # # Register Payment Service
# curl -i -X POST $KONG_ADMIN_URL/services/ \
#   --data "name=payment-service" \
#   --data "url=http://host.docker.internal:8011"
# # Register Payment Service routes
# curl -i -X POST $KONG_ADMIN_URL/services/payment-service/routes \
#   --data "paths[]=/payment-service" \
#   --data "strip_path=true"

# echo "All services registered successfully!"
