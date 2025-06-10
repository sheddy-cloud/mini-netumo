#!/bin/bash

# health_check.sh
# Logs and restarts unhealthy Docker containers in the Mini Netumo stack

LOG_FILE="/var/log/mini-netumo-health.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Running health check..." >> "$LOG_FILE"

# List of expected service names (adjust if different)
SERVICES=("load-balancer" "frontend-1" "frontend-2" "frontend-3" "api" "worker" "redis" "db")

for SERVICE in "${SERVICES[@]}"; do
    CONTAINER=$(docker ps --filter "name=${SERVICE}" --format "{{.Names}}")

# If the container is not running, it logs a warning and skips to the next one.
    if [ -z "$CONTAINER" ]; then
        echo "[$DATE] ALERT: $SERVICE container not running." >> "$LOG_FILE"
        continue
    fi

# Gets the health status of the container using Docker inspect.
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER" 2>/dev/null)

    if [ "$STATUS" == "healthy" ]; then
        echo "[$DATE] $SERVICE is healthy." >> "$LOG_FILE"
    else
        echo "[$DATE] ALERT: $SERVICE is unhealthy (status: $STATUS). Restarting..." >> "$LOG_FILE"
        docker restart "$CONTAINER" >> "$LOG_FILE" 2>&1
    fi
done
