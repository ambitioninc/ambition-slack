from celery.decorators import periodic_task
from celery.task.schedules import crontab

from ambition_slack.digest.morning_digest import send_digest_to_all_slack_users


# Execute this task at 14:00 UTC (9:00 or 10:00 EST every day of the week)
@periodic_task(run_every=(crontab(hour="14,15", minute="0,20", day_of_week="1,2,3,4,5")), ignore_result=True)
def generate_morning_digests():
    send_digest_to_all_slack_users()
