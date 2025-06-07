from fastapi import APIRouter

from backend.celery import celery_app

router = APIRouter()

@router.get("/task-status/{task_id}")
def get_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
