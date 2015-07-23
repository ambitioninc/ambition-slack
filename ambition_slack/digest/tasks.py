from celery.decorators import periodic_task
from celery.task.schedules import crontab


# Execute this task at 14:00 UTC (9:00 or 10:00 EST every day of the week)
@periodic_task(run_every=(crontab(hour="14", minute="0", day_of_week="1,2,3,4,5")), ignore_result=True)
def generate_digest():
    pass
