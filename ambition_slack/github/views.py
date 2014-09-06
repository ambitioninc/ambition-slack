import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
from manager_utils import get_or_none
import slack
import slack.chat
import slack.users

from ambition_slack.github.models import GithubUser


LOG = logging.getLogger('console_logger')


class GithubView(View):
    def get(self, *args, **kwargs):
        slack.api_token = os.environ['SLACK_API_TOKEN']
        #LOG.info('slack token', os.environ['SLACK_API_TOKEN'])
        #LOG.info('slack users', slack.users.list())

        #gh = Github(os.environ['GITHUB_USER'], os.environ['GITHUB_PASS'])
        #LOG.info('github user', gh.get_user())

        slack.api_token = os.environ['SLACK_API_TOKEN']
        slack.chat.post_message('@wesleykendall', 'New PR!', username='wesleykendall')

        return HttpResponse('Done token {0} {1}'.format(os.environ['SLACK_API_TOKEN'], slack.users.list()))

    def handle_pull_request(self, payload):
        """
        Handles a new pull request and notifies the proper slack user.
        """
        slack.api_token = os.environ['SLACK_API_TOKEN']

        # Find out who made the pull request
        creator = GithubUser.objects.get(username=payload['pull_request']['user']['login'])

        action = payload['action']
        if action == 'closed':
            action = 'merged' if payload['pull_request']['merged'] else action

        if action in ('opened', 'reopened', 'closed', 'merged'):
            assignee = get_or_none(GithubUser.objects, username=payload['pull_request']['assignee'])

            # Search the body of the pull request for a mention
            github_users = GithubUser.objects.select_related('slack_user')
            for gh_user in github_users:
                if '@{}'.format(gh_user.username) in payload['pull_request']['body'] or assignee == gh_user:
                    slack.chat.post_message(
                        '@{}'.format(gh_user.slack_user.username),
                        '{} {} *{}* ({})'.format(
                            creator.slack_user.name, action, payload['pull_request']['title'].strip(),
                            payload['pull_request']['html_url']),
                        username='github')
        elif action == 'assigned':
            LOG.info('assigned {}'.format(payload['pull_request']['assignee']))
            gh_user = GithubUser.objects.get(username=payload['pull_request']['assignee'])
            slack.chat.post_message(
                '@{}'.format(gh_user.slack_user.username),
                '{} {} you to *{}* ({})'.format(
                    creator.slack_user.name, action, payload['pull_request']['title'].strip(),
                    payload['pull_request']['html_url']),
                username='github')

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)

        if payload.get('pull_request'):  # and payload.get('action') == 'opened':
            self.handle_pull_request(payload)
            LOG.info('New PR opened with body {0}'.format(payload['pull_request']['body']))

        return HttpResponse()
