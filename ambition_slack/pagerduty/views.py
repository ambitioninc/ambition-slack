import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
import slack
import slack.chat
import slack.users


slack.api_token = os.environ['SLACK_API_TOKEN']
LOG = logging.getLogger('console_logger')


class PagerdutyView(View):

    def get(self, *args, **kwargs):
        return HttpResponse('Pagerduty')

    def post(self, request, *args, **kwargs):
        """
        Handles webhook posts from Pagerduty
        """
        payload = json.loads(request.body)

        for message in payload['messages']:
            if message['type'] == 'incident.trigger':
                names = [
                    assigned_to['object']['name']
                    for assigned_to in message['data']['incident']['assigned_to']
                ]
                slack.chat.post_message(
                    '#support',
                    'New Pagerduty Ticket assigned to {}. Incident details - {}. Trigger details - {}'.format(
                        ', '.join(names),
                        message['data']['incident']['html_url'],
                        message['data']['incident']['trigger_details_html_url']),
                    username='pagerduty')

            elif message['type'] == 'incident.resolve':
                slack.chat.post_message(
                    '#support',
                    'Pagerduty Ticket is now Resolved. Thank you. Incident details - {}. Trigger details - {}'.format(
                        message['data']['incident']['html_url'],
                        message['data']['incident']['trigger_details_html_url']),
                    username='pagerduty')
        return HttpResponse()
