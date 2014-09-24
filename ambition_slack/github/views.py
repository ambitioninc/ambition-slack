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


slack.api_token = os.environ['SLACK_API_TOKEN']
LOG = logging.getLogger('console_logger')


class GithubView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Github')

    def get_assignee(self, payload):
        assignee = payload['pull_request']['assignee']
        if assignee:
            return get_or_none(GithubUser.objects, username=assignee['login'])

    def handle_pull_request_repo_action(self, payload):
        """
        Handles a new pull request action on a repo (open, close, merge, assign) and notifies the proper slack user.
        """
        # Find out who made the action and who was assigned
        sender = GithubUser.objects.get(username=payload['sender']['login'])
        assignee = self.get_assignee(payload)

        action = payload['action']
        if action == 'closed':
            # Distinguish if the action was closed or merged
            action = 'merged' if payload['pull_request']['merged'] else action
        if action in ('opened', 'reopened', 'closed', 'merged'):
            # In this case, a PR was opened, reopened, closed or merged
            github_users = GithubUser.objects.select_related('slack_user')
            for gh_user in github_users:
                if '@{}'.format(gh_user.username) in payload['pull_request']['body'].lower() or assignee == gh_user:
                    slack.chat.post_message(
                        '@{}'.format(gh_user.slack_user.username),
                        'Pull request {} by {} - ({})'.format(
                            action, sender.slack_user.name, payload['pull_request']['html_url']),
                        username='github')
        elif action in ('assigned',):
            # In this case, a new person was assigned to the PR
            slack.chat.post_message(
                '@{}'.format(assignee.slack_user.username),
                'Pull request {} to you by {} - ({})'.format(
                    action, sender.slack_user.name, payload['pull_request']['html_url']),
                username='github')

    def handle_pull_request_comment_action(self, payload):
        """
        Handles a comment on a pull request and notifies the proper slack user if they were tagged.
        """
        sender = GithubUser.objects.get(username=payload['sender']['login'])

        # In this case, a comment was created on the PR. Notify anyone tagged.
        github_users = GithubUser.objects.select_related('slack_user')
        for gh_user in github_users:
            if '@{}'.format(gh_user.username) in payload['comment']['body'].lower():
                slack.chat.post_message(
                    '@{}'.format(gh_user.slack_user.username),
                    'Pull request comment from {} - ({})'.format(
                        sender.slack_user.name, payload['issue']['pull_request']['html_url']),
                    username='github')

    def post(self, request, *args, **kwargs):
        """
        Handles webhook posts from Github
        """
        payload = json.loads(request.body)

        if 'pull_request' in payload and payload['action'] in ('opened', 'reopened', 'closed', 'merged', 'assigned'):
            self.handle_pull_request_repo_action(payload)
        elif 'issue' in payload and 'pull_request' in payload['issue'] and payload['action'] == 'created':
            self.handle_pull_request_comment_action(payload)

        return HttpResponse()
