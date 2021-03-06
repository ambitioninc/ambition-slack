from datetime import datetime
import json
import logging
import os

import slack
import slack.chat
from pytz import utc as utc_tz

from ambition_slack.github.issue import fetch_assigned_pull_requests, fetch_pull_requests_with_mention
from ambition_slack.slack.models import SlackUser


# The time (in user local timezone) to send the morning digest
DIGEST_HOUR = 10

LOG = logging.getLogger(__name__)

slack.api_token = os.environ['SLACK_API_TOKEN']


class MorningDigest(object):
    """
    This class handles constructing and sending a morning digest customized for each developer.
    """
    def _build_channel_name(self, slack_user):
        return '@{0}'.format(slack_user.username)

    def _build_digest_message(self, slack_user):
        return 'Good morning {0}'.format(slack_user.username)

    def _construct_attachments(self, slack_user):
        """
        Construct the actual digest content.
        """
        attachments = []

        # Add reminder to post scrum in #engineering
        attachments.append({
            'text': 'Remember to post Standup in #engineering',
            'color': 'good',
        })

        # Add reminders about open pull requests
        attachments.append({
            'text': 'Assigned pull requests',
            'color': 'good',
            'fields': [
                {
                    'title': issue.title,
                    'value': issue.pull_request_link,
                }
                for issue in fetch_assigned_pull_requests(slack_user.github_user)
            ]
        })
        attachments.append({
            'text': '@mentions',
            'color': 'good',
            'fields': [
                {
                    'title': issue.title,
                    'value': issue.pull_request_link,
                }
                for issue in fetch_pull_requests_with_mention(slack_user.github_user)
            ]
        })

        # TODO: Add reminder about any all day events

        return attachments

    def _construct_message_kwargs(self, slack_user):
        return {
            'username': 'DigestBot',
            'attachments': json.dumps(self._construct_attachments(slack_user)),
        }

    def post_to_slack(self, slack_user):
        """
        Post the digest to slack.
        """
        if not slack_user:
            LOG.error('post_to_slack called when slack_user = None')
            return

        # TODO: if the user is out of the office (check calendar) then don't post anything for them
        slack.chat.post_message(
            self._build_channel_name(slack_user), self._build_digest_message(slack_user),
            **self._construct_message_kwargs(slack_user))


def get_digest_users():
    """
    Based on the DIGEST_USERS env variable, send morning digest to all users or a subset.
    """
    digest_users_env_val = os.environ['DIGEST_USERS']
    slack_users = SlackUser.objects.filter(expects_morning_digest=True)

    if digest_users_env_val != '*':
        digest_user_list = digest_users_env_val.split(',')
        slack_users = SlackUser.objects.filter(username__in=digest_user_list)

        if slack_users.count() == 0:
            LOG.warning('No slack users selected')

    return slack_users


def is_weekend(localtime):
    return localtime.weekday() in [5, 6]


def is_digest_hour(localtime):
    return localtime.hour == DIGEST_HOUR


def time_for_user_digest(slack_user):
    """
    One should only send a digest when the time is right in their timezone.
    """
    localtime = slack_user.time_zone.normalize(utc_tz.localize(datetime.utcnow()))

    return not is_weekend(localtime) and is_digest_hour(localtime)


def send_digest_to_all_slack_users():
    """
    Create and post a morning digest for all slack users.
    """
    for su in get_digest_users():
        if time_for_user_digest(su):
            try:
                MorningDigest().post_to_slack(su)
            except Exception as e:
                LOG.error('Could not send digest to "{0}"; exception: {1}'.format(su.username, str(e)))
