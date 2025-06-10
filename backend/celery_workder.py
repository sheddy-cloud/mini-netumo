# Explicitly import tasks so they are registered
import api.tasks.tasks
from celery_app import celery_app
