#!/bin/bash

# update_services.sh
# Pulls latest Docker images and restarts the stack

LOG_FILE="/var/log/mini-netumo-update.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

{
    echo "[$DATE] Pulling latest Docker images..."
    docker-compose pull 2>&1

    echo "[$DATE] Restarting services..."
    docker-compose up -d 2>&1

    echo "[$DATE] Update complete."
} >> "$LOG_FILE"
