#!/bin/bash

# update_services.sh
# Pulls latest Docker images and restarts the stack

LOG_FILE="/var/log/mini-netumo-update.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

{
    echo "[$DATE] Pulling latest Docker images..."
} >>"$LOG_FILE"

docker-compose pull >>"$LOG_FILE" 2>&1

{
    echo "[$DATE] Restarting services..."
} >>"$LOG_FILE"
docker-compose up -d >>"$LOG_FILE" 2>&1
{
    echo "[$DATE] Update complete."
} >>"$LOG_FILE"
