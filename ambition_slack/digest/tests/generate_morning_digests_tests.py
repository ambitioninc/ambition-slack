from django.core.management import call_command
from django.test import TestCase
from mock import patch


class GenerateDigestTests(TestCase):
    @patch(
        'ambition_slack.digest.management.commands.generate_morning_digests.send_digest_to_all_slack_users',
        spec_set=True)
    def test_run(self, send_digest_to_all_slack_users):
        # Run code
        call_command('generate_morning_digests')

        # Verify expectations
        self.assertTrue(1, send_digest_to_all_slack_users.call_count)
