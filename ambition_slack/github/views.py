import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
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
        # Find out who made the pull request
        creator = GithubUser.objects.get(username=payload['pull_request']['user']['login'])

        # Search the body of the pull request for a mention
        github_users = GithubUser.objects.select_related('slack_user')
        for gh_user in github_users:
            if '@{}'.format(gh_user.username) in payload['pull_request']['body']:
                # If someone was mentioned, send them a slack message.
                LOG.info('Notifying Slack User {} of PR'.format(gh_user.slack_user.username))
                LOG.info('Creator {}'.format(creator.slack_user.name))
                LOG.info('Action {}'.format(payload['action']))
                LOG.info('URL {}'.format(payload['pull_request']['url']))
                LOG.info('Body {}'.format(payload['pull_request']['body']))
                slack.api_token = os.environ['SLACK_API_TOKEN']
                slack.chat.post_message(
                    '@{}'.format(gh_user.slack_user.username),
                    '{} {} {}.\n```{}```'.format(
                        creator.slack_user.name, payload['action'], payload['pull_request']['html_url'],
                        payload['pull_request']['body']),
                    username='github')

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)

        if payload.get('pull_request'):  # and payload.get('action') == 'opened':
            self.handle_pull_request(payload)
            LOG.info('New PR opened with body {0}'.format(payload['pull_request']['body']))

        return HttpResponse()
