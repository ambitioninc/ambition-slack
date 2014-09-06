import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
from github import Github
import slack
import slack.chat
import slack.users


LOG = logging.getLogger('console_logger')


class GithubView(View):
    def get(self, *args, **kwargs):
        print os.environ['SLACK_API_TOKEN']
        slack.api_token = os.environ['SLACK_API_TOKEN']
        print 'slack users', slack.users.list()

        gh = Github(os.environ['GITHUB_USER'], os.environ['GITHUB_PASS'])
        print 'github user', gh.get_user()

        return HttpResponse()

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)

        if payload.get('pull_request') and payload.get('action') == 'opened':
            LOG.info('New PR opened with body {0}'.format(payload['pull_request']['body']))

        return HttpResponse()
