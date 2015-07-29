import json
import os

from django.test import TestCase
from django_dynamic_fixture import G
from mock import call, patch
import slack.users

from ambition_slack.digest.morning_digest import MorningDigest, send_digest_to_all_slack_users
from ambition_slack.slack.models import SlackUser


class MorningDigestTests(TestCase):
    def setUp(self):
        super(MorningDigestTests, self).setUp()

        self.slack_user_1 = G(SlackUser)

    def test_channel_name(self):
        self.assertEquals('@{0}'.format(self.slack_user_1.username), MorningDigest(self.slack_user_1).channel_name)

    def test_construct_message_kwargs(self):
        # Setup scenario
        md = MorningDigest(self.slack_user_1)

        # Run code
        attachments = md._construct_message_kwargs()

        # Verify expectations
        self.assertEquals({
            'username': 'DigestBot',
            'attachments': json.dumps([{
                'color': 'good',
                'text': 'Remember to post Standup in #engineering',
            }]),
        }, attachments)

    @patch.object(MorningDigest, '_construct_attachments', spec_set=True, return_value='fake-return')
    @patch.object(slack.chat, 'post_message', spec_set=True)
    def test_post_to_slack(self, post_message, construct_attachments):
        # Setup scenario
        md = MorningDigest(self.slack_user_1)

        # Run code
        md.post_to_slack()

        # Verify expectations
        post_message.assert_called_once_with(
            md.channel_name, md.message, username='DigestBot',
            attachments=json.dumps(construct_attachments.return_value))

    @patch.object(slack.chat, 'post_message', spec_set=True)
    def test_post_to_slack_gracefully_handles_none_slack_user(self, post_message):
        # Run code
        MorningDigest(None).post_to_slack()

        # Verify expectations
        self.assertFalse(post_message.called)

    @patch('ambition_slack.digest.morning_digest.MorningDigest', spec_set=True)
    def test_send_digest_to_all_slack_users(self, morning_digest):
        """
        Verify that we construct and send a digest to all slack users.
        """
        # Setup scenario
        slack_user_2 = G(SlackUser)
        os.environ['DIGEST_USERS'] = '*'

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        morning_digest.assert_has_calls([call(self.slack_user_1), call(slack_user_2)], any_order=True)
        self.assertEquals(2, morning_digest.return_value.post_to_slack.call_count)

    @patch('ambition_slack.digest.morning_digest.MorningDigest', spec_set=True)
    def test_send_digest_to_subset_of_slack_users(self, morning_digest):
        """
        Verify that we construct and send a digest to only the slack users specified by DIGEST_USERS.
        """
        # Setup scenario
        slack_user_2 = G(SlackUser)
        G(SlackUser)
        os.environ['DIGEST_USERS'] = ','.join([self.slack_user_1.username, slack_user_2.username])

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        morning_digest.assert_has_calls([call(self.slack_user_1), call(slack_user_2)], any_order=True)
        self.assertEquals(2, morning_digest.return_value.post_to_slack.call_count)

    @patch('ambition_slack.digest.morning_digest.LOG', spec_set=True)
    @patch('ambition_slack.digest.morning_digest.MorningDigest', spec_set=True)
    def test_send_digest_handles_invalid_env_var(self, morning_digest, log):
        """
        Verify that we gracefully handle a miconfigured digest_users variable.
        """
        # Setup scenario
        os.environ['DIGEST_USERS'] = ''

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        self.assertFalse(morning_digest.called)
        self.assertEquals(0, morning_digest.return_value.post_to_slack.call_count)
        log.warning.assert_called_once_with('No slack users selected')
