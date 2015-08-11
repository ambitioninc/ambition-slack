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
from ambition_slack.github.payload import GithubPayload


slack.api_token = os.environ['SLACK_API_TOKEN']
LOG = logging.getLogger('console_logger')


class GithubView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Github')

    def handle_pull_request_repo_action(self, payload):
        """
        Handles a new pull request action on a repo (open, close, merge, assign) and notifies the proper slack user.
        """
        # Find out who made the action and who was assigned
        sender = GithubUser.objects.get(username__iexact=payload.sender_login)
        assignee = get_or_none(GithubUser.objects, username__iexact=payload.assignee_login)

        if payload.is_opened_or_merged or payload.is_closed:
            # In this case, a PR was opened, reopened, closed or merged
            github_users = GithubUser.objects.select_related('slack_user')
            for gh_user in github_users:
                if payload.mentions_user(gh_user.username) or assignee == gh_user:
                    slack.chat.post_message(
                        '@{}'.format(gh_user.slack_user.username),
                        'Pull request {} by {} - ({})'.format(
                            payload.action, sender.slack_user.name, payload.pull_request_html_url),
                        username='github')
        elif payload.is_assigned:
            # In this case, a new person was assigned to the PR
            slack.chat.post_message(
                '@{}'.format(assignee.slack_user.username),
                'Pull request {} to you by {} - ({})'.format(
                    payload.action, sender.slack_user.name, payload.pull_request_html_url),
                username='github')

    def handle_pull_request_comment_action(self, payload):
        """
        Handles a comment on a pull request and notifies the proper slack user if they were tagged.
        """
        sender = GithubUser.objects.get(username__iexact=payload.sender_login)

        # In this case, a comment was created on the PR. Notify anyone tagged.
        github_users = GithubUser.objects.select_related('slack_user')
        for gh_user in github_users:
            if payload.mentions_user(gh_user.username):
                slack.chat.post_message(
                    '@{}'.format(gh_user.slack_user.username),
                    'Pull request comment from {} - ({})'.format(
                        sender.slack_user.name, payload.pull_request_comment),
                    username='github')

    def post(self, request, *args, **kwargs):
        """
        Handles webhook posts from Github
        """
        payload = GithubPayload(json.loads(request.body))

        if payload.is_pull_request_action:
            self.handle_pull_request_repo_action(payload)
        elif payload.is_pull_request_comment:
            self.handle_pull_request_comment_action(payload)

        return HttpResponse()
