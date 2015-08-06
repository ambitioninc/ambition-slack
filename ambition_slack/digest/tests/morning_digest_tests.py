from datetime import datetime
import json
import os

from django.test import TestCase
from django_dynamic_fixture import G
from freezegun import freeze_time
from mock import call, patch
import slack.users

from ambition_slack.digest.morning_digest import (
    MorningDigest, get_digest_users, send_digest_to_all_slack_users, time_for_user_digest
)
from ambition_slack.slack.models import SlackUser


class MorningDigestTests(TestCase):
    def setUp(self):
        super(MorningDigestTests, self).setUp()

        self.slack_user_1 = G(SlackUser, time_zone='US/Eastern', expects_morning_digest=True)

    def test_build_channel_name(self):
        self.assertEquals(
            '@{0}'.format(self.slack_user_1.username), MorningDigest()._build_channel_name(self.slack_user_1))

    def test_construct_message_kwargs(self):
        # Setup scenario
        md = MorningDigest()

        # Run code
        attachments = md._construct_message_kwargs(self.slack_user_1)

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
        md = MorningDigest()

        # Run code
        md.post_to_slack(self.slack_user_1)

        # Verify expectations
        post_message.assert_called_once_with(
            md._build_channel_name(self.slack_user_1), md._build_digest_message(self.slack_user_1),
            username='DigestBot', attachments=json.dumps(construct_attachments.return_value))

    @patch.object(slack.chat, 'post_message', spec_set=True)
    def test_post_to_slack_gracefully_handles_none_slack_user(self, post_message):
        # Run code
        MorningDigest().post_to_slack(None)

        # Verify expectations
        self.assertFalse(post_message.called)

    @freeze_time(datetime(2015, 8, 3, 14))
    def test_time_for_user_digest_returns_true(self):
        self.assertTrue(time_for_user_digest(self.slack_user_1))

    @freeze_time(datetime(2015, 8, 3, 13))
    def test_time_for_user_digest_returns_false(self):
        self.assertFalse(time_for_user_digest(self.slack_user_1))

    def test_get_digest_users(self):
        """
        Verify get_digest_users only returns users who expect a morning digest.
        """
        # Setup scenario
        G(SlackUser, expects_morning_digest=False)
        os.environ['DIGEST_USERS'] = '*'

        # Run code and verify expectations
        self.assertEquals([self.slack_user_1], list(get_digest_users()))

    @patch('ambition_slack.digest.morning_digest.time_for_user_digest', spec_set=True, return_value=True)
    @patch.object(MorningDigest, 'post_to_slack', spec_set=True)
    def test_send_digest_to_all_slack_users(self, post_to_slack, time_for_user_digest):
        """
        Verify that we construct and send a digest to all slack users.
        """
        # Setup scenario
        slack_user_2 = G(SlackUser, expects_morning_digest=True)
        os.environ['DIGEST_USERS'] = '*'

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        post_to_slack.assert_has_calls([call(self.slack_user_1), call(slack_user_2)], any_order=True)
        self.assertEquals(2, post_to_slack.call_count)

    @patch('ambition_slack.digest.morning_digest.time_for_user_digest', spec_set=True, return_value=True)
    @patch.object(MorningDigest, 'post_to_slack', spec_set=True)
    def test_send_digest_to_subset_of_slack_users_based_on_env_var(self, post_to_slack, time_for_user_digest):
        """
        Verify that we construct and send a digest to only the slack users specified by DIGEST_USERS.
        """
        # Setup scenario
        slack_user_2 = G(SlackUser, expects_morning_digest=True)
        G(SlackUser, expects_morning_digest=True)
        os.environ['DIGEST_USERS'] = ','.join([self.slack_user_1.username, slack_user_2.username])

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        post_to_slack.assert_has_calls([call(self.slack_user_1), call(slack_user_2)], any_order=True)
        self.assertEquals(2, post_to_slack.call_count)

    @patch('ambition_slack.digest.morning_digest.time_for_user_digest', spec_set=True, return_value=True)
    @patch.object(MorningDigest, 'post_to_slack', spec_set=True)
    def test_send_digest_to_subset_of_slack_users_based_on_tz(self, post_to_slack, time_for_user_digest):
        """
        Verify that we construct and send a digest to only the slack users specified by DIGEST_USERS.
        """
        # Setup scenario
        slack_user_2 = G(SlackUser, expects_morning_digest=True)
        os.environ['DIGEST_USERS'] = ','.join([self.slack_user_1.username, slack_user_2.username])

        def side_effect(u):
            # Only the first user is in the appropriate timezone
            return (u == self.slack_user_1)

        time_for_user_digest.side_effect = side_effect

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        post_to_slack.assert_called_once_with(self.slack_user_1)

    @patch('ambition_slack.digest.morning_digest.time_for_user_digest', spec_set=True, return_value=True)
    @patch('ambition_slack.digest.morning_digest.LOG', spec_set=True)
    @patch('ambition_slack.digest.morning_digest.MorningDigest', spec_set=True)
    def test_send_digest_handles_invalid_env_var(self, morning_digest, log, time_for_user_digest):
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

    @patch('ambition_slack.digest.morning_digest.time_for_user_digest', spec_set=True, return_value=True)
    @patch('ambition_slack.digest.morning_digest.LOG', spec_set=True)
    @patch('ambition_slack.digest.morning_digest.MorningDigest', spec_set=True)
    def test_send_digest_handles_exception(self, morning_digest, log, time_for_user_digest):
        """
        Verify that we gracefully handle an exception when posting a digest.
        """
        # Setup scenario
        os.environ['DIGEST_USERS'] = '*'
        e = Exception()
        morning_digest.return_value.post_to_slack.side_effect = e

        # Run code
        send_digest_to_all_slack_users()

        # Verify expectations
        self.assertTrue(morning_digest.called)
        self.assertEquals(1, morning_digest.return_value.post_to_slack.call_count)
        log.error.assert_called_once_with(
            'Could not send digest to "{0}"; exception: {1}'.format(self.slack_user_1.username, str(e)))
