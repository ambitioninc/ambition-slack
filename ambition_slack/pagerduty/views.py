import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
import slack
import slack.chat
import slack.users

from ambition_slack.pagerduty.models import AlertReceipt


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
            alert_type = message['type']
            incident_uid = message['data']['incident']['id']
            if not AlertReceipt.objects.create_alert_receipt(alert_type, incident_uid):
                # We have already had an alert of this posted to slack, so ignore it
                continue

            if alert_type == 'incident.trigger':
                names = [
                    assigned_to['object']['name']
                    for assigned_to in message['data']['incident']['assigned_to']
                ]
                multi_names = ', '.join(names)
                client = message['data']['incident']['trigger_summary_data']['client']
                trigger_style = [{
                    'fallback': 'pagerduty alert',
                    'color': '#c52929',
                    'fields': [{
                        'title': 'Client',
                        'value': client, 'short': True
                    }, {
                        'title': 'Assigned To:',
                        'value': multi_names, 'short': True
                    }]
                }]
                t_style = json.dumps(trigger_style)
                slack.chat.post_message(
                    '#support',
                    '<{}|Incident details> | <{}|Trigger details>'.format(
                        message['data']['incident']['html_url'],
                        message['data']['incident']['trigger_details_html_url']),
                    attachments=t_style,
                    username='pagerduty',
                    icon_url=icon)

            elif alert_type == 'incident.resolve':
                names = message['data']['incident']['resolved_by_user']['name']
                client = message['data']['incident']['trigger_summary_data']['client']
                resolve_style = [{
                    'fallback': 'pagerduty alert',
                    'color': '228b22',
                    'fields': [{
                        'title': 'Client',
                        'value': client, 'short': True
                    }, {
                        'title': 'Resolved by:',
                        'value': names, 'short': True
                    }]
                }]
                r_style = json.dumps(resolve_style)
                slack.chat.post_message(
                    '#support',
                    '*Resolved* - <{}|Incident details> | <{}|Trigger details>'.format(
                        message['data']['incident']['html_url'],
                        message['data']['incident']['trigger_details_html_url']),
                    attachments=r_style,
                    username='pagerduty',
                    icon_url=icon)
        return HttpResponse()
