from celery.schedules import schedule

beat_schedule = {
    'run-monitor-worker-every-10-seconds': {
        'task': 'tasks.monitor_target',
        'schedule': schedule(10.0),
    },
    'run-certificate-check-every-10-seconds': {
        'task': 'tasks.cert_check_target',
        'schedule': schedule(10.0),
    },
}
