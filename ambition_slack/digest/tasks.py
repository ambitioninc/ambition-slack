from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.core.mail import EmailMultiAlternatives


# Execute this task at 14:00 UTC (9:00 or 10:00 EST every day of the week)
@periodic_task(run_every=(crontab(hour="14", minute="0", day_of_week="1,2,3,4,5")), ignore_result=True)
def generate_digest():
    pass


@periodic_task(
    run_every=(crontab(hour="*", minute="0,10,15,20,25,30,35,40,45,50,55", day_of_week="1,2,3,4,5")),
    ignore_result=True)
def this_is_a_test():
    EmailMultiAlternatives('Celery test', 'This is a test', '', ['joshmarlow@gmail.com']).send()
