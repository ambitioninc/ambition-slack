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
        icon = 'https://pbs.twimg.com/profile_images/482648331181490177/4X_QI2Vu_400x400.png'
        for message in payload['messages']:
            if message['type'] == 'incident.trigger':
                names = [
                    assigned_to['object']['name']
                    for assigned_to in message['data']['incident']['assigned_to']
                ]
                multi_names = ', '.join(names)
                client = message['data']['incident']['trigger_summary_data']['client']
                trigger_style = [{'fallback': 'pagerduty alert',
                                  'color': '#c52929',
                                  'fields': [{'title': 'Client', 'value': client, 'short': True},
                                             {'title': 'Assigned To:', 'value': multi_names, 'short': True}]}]
                t_style = json.dumps(trigger_style)
                slack.chat.post_message(
                    '@jody',
                    'Incident details: ({}) Trigger details: ({})'
                    .format(
                        message['data']['incident']['html_url'],
                        message['data']['incident']['trigger_details_html_url']),
                    attachments=t_style,
                    username='pagerduty',
                    icon_url=icon,)

            elif message['type'] == 'incident.resolve':
                attachments = [{'fallback': 'pagerduty alert', 'color': '228b22'}]
                slack.chat.post_message(
                    attachments,
                    '#support',
                    'Pagerduty Ticket is now resolved, Thank you. Client {} Incident details - {}. Trigger details - {}'
                    .format(
                        message['data']['incident']['trigger_summary_data']['client'],
                        message['data']['incident']['html_url'],
                        message['data']['incident']['trigger_details_html_url']),
                    username='pagerduty',
                    icon_url=pd_icon_url)
        return HttpResponse()
