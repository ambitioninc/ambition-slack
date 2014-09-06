import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
from github import Github
from manager_utils import get_or_none
import slack
import slack.chat
import slack.users

from ambition_slack.github.models import GithubUser
from ambition_slack.slack.models import SlackUser


LOG = logging.getLogger('console_logger')


class GithubView(View):
    def get(self, *args, **kwargs):
        slack.api_token = os.environ['SLACK_API_TOKEN']
        LOG.info('slack token', os.environ['SLACK_API_TOKEN'])
        LOG.info('slack users', slack.users.list())

        gh = Github(os.environ['GITHUB_USER'], os.environ['GITHUB_PASS'])
        LOG.info('github user', gh.get_user())

        return HttpResponse('Done')

    def handle_pull_request(self, payload):
        """
        Handles a new pull request and notifies the proper slack user.
        """
        # Search the body of the pull request for a mention
        body = payload['pull_request']['body']
        github_users_emails = GithubUser.objects.values_list('username', 'email')

        for gh_user, gh_email in github_users_emails:
            if '@{}'.format(gh_user) in body:
                slack_user = get_or_none(SlackUser.objects, email=gh_email)
                if slack_user:
                    LOG.info('Notifying Slack User {} of PR'.format(slack_user.username))

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)

        if payload.get('pull_request'):  # and payload.get('action') == 'opened':
            self.handle_pull_request(payload)
            LOG.info('New PR opened with body {0}'.format(payload['pull_request']['body']))

        return HttpResponse()
