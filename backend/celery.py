# backend/celery.py

import os

from celery import Celery

celery_app = Celery(
    "mini_netumo",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND")
)

celery_app.conf.task_routes = {
    "tasks.*": {"queue": "default"},
}
