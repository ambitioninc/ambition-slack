from datetime import datetime

from django.core.management.base import BaseCommand

from ambition_slack.digest.morning_digest import send_digest_to_all_slack_users


class Command(BaseCommand):
    help = 'Generate and send a morning digest for each developer'

    usage_string = 'usage: generate_digest'

    def handle(self, *args, **options):
        send_digest_to_all_slack_users()

    def is_weekday(self):
        return (datetime.today().weekday() < 5)
