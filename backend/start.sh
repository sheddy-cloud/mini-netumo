#!/bin/bash

# Start Celery Worker with event monitoring in the background
python -m api.init_db &

python -m celery -A celery_app worker --loglevel=info -E &

# Start FastAPI (replace with actual import path if needed)
exec uvicorn main:app --host=0.0.0.0 --port=80
