from django.test import TestCase
from django.test.utils import override_settings
from mock import patch

from ambition_slack.digest.tasks import generate_morning_digests


class GenerateDigestTest(TestCase):
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    @patch('ambition_slack.digest.tasks.send_digest_to_all_slack_users', spec_set=True)
    def test_delay(self, send_digest_to_all_slack_users):
        # Run code
        generate_morning_digests.delay()

        # Verify expectations
        self.assertTrue(send_digest_to_all_slack_users.called)
