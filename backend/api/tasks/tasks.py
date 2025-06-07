# backend/tasks/tasks.py

import time

from backend.celery import celery_app


@celery_app.task
def sample_task(duration: int):
    time.sleep(duration)
    return f"Task completed after {duration} seconds"
