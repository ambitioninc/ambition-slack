from datetime import datetime

from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from mock import patch

from ambition_slack.digest.management.commands.generate_morning_digests import Command


class GenerateDigestTests(TestCase):
    @patch(
        'ambition_slack.digest.management.commands.generate_morning_digests.send_digest_to_all_slack_users',
        spec_set=True)
    @patch.object(Command, 'is_weekday', spec_set=True, return_value=True)
    def test_run(self, send_digest_to_all_slack_users, is_weekday):
        # Run code
        call_command('generate_morning_digests')

        # Verify expectations
        self.assertTrue(1, send_digest_to_all_slack_users.call_count)

    @patch(
        'ambition_slack.digest.management.commands.generate_morning_digests.send_digest_to_all_slack_users',
        spec_set=True)
    @patch.object(Command, 'is_weekday', spec_set=True, return_value=False)
    def test_run_on_weekend(self, send_digest_to_all_slack_users, is_weekday):
        # Run code
        call_command('generate_morning_digests')

        # Verify expectations
        self.assertFalse(send_digest_to_all_slack_users.called)

    def test_is_weekday_monday(self):
        with freeze_time(datetime(2015, 8, 3)):
            self.assertTrue(Command().is_weekday())

    def test_is_weekday_tuesday(self):
        with freeze_time(datetime(2015, 8, 4)):
            self.assertTrue(Command().is_weekday())

    def test_is_weekday_wednesday(self):
        with freeze_time(datetime(2015, 8, 5)):
            self.assertTrue(Command().is_weekday())

    def test_is_weekday_thursday(self):
        with freeze_time(datetime(2015, 8, 6)):
            self.assertTrue(Command().is_weekday())

    def test_is_weekday_friday(self):
        with freeze_time(datetime(2015, 8, 7)):
            self.assertTrue(Command().is_weekday())

    def test_is_weekday_saturday(self):
        with freeze_time(datetime(2015, 8, 8)):
            self.assertFalse(Command().is_weekday())

    def test_is_weekday_sunday(self):
        with freeze_time(datetime(2015, 8, 9)):
            self.assertFalse(Command().is_weekday())
