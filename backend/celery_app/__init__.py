import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

celery_app = Celery(
    "mini_netumo",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND")
)

# Basic config
celery_app.conf.timezone = 'UTC'
celery_app.conf.task_routes = {
    "api.tasks.tasks.*": {"queue": "default"},
}

celery_app.autodiscover_tasks(['api.tasks'])
