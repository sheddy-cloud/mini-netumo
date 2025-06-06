#!/bin/sh

# Start JSON Server in background, using /app/database/db.json (mounted volume)
json-server --watch /app/db.json --port 3000 &
serve -s dist -l 80
