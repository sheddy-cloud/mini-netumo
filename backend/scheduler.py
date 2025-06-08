# backend/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from celery_app import celery_app

scheduler = BackgroundScheduler()
scheduler.start()


def schedule_target_monitoring(target_id: int, url: str):
    job_id = f"monitor_{target_id}"
    scheduler.add_job(
        func=celery_app.send_task,
        trigger="interval",
        seconds=30,
        args=["tasks.monitor_target", [target_id, url]],
        id=job_id,
        replace_existing=True,
    )
    print(f"✅ Scheduled job: {job_id}")


def schedule_cert_check(target_id: int, url: str):
    job_id = f"certcheck_{target_id}"
    scheduler.add_job(
        func=celery_app.send_task,
        trigger="interval",
        seconds=30,
        args=["tasks.cert_check_target", [target_id, url]],
        id=job_id,
        replace_existing=True,
    )
    print(f"✅ Scheduled job: {job_id}")

def cancel_target_jobs(target_id: int):
    for suffix in ["monitor", "certcheck"]:
        job_id = f"{suffix}_{target_id}"
        try:
            scheduler.remove_job(job_id)
            print(f"Cancelled job: {job_id}")
        except Exception as e:
            print(f"Job {job_id} not found or already removed: {e}")
