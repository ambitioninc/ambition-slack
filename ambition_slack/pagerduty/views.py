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
    ICON = 'https://pbs.twimg.com/profile_images/482648331181490177/4X_QI2Vu_400x400.png'

    def get(self, *args, **kwargs):
        return HttpResponse('Pagerduty')

    def get_client_from_message(self, message):
        if (
                'trigger_summary_data' in message['data']['incident'] and
                'client' in message['data']['incident']['trigger_summary_data']):
            return message['data']['incident']['trigger_summary_data']['client']
        else:
            return None

    def get_description_from_message(self, message):
        if (
                'trigger_summary_data' in message['data']['incident'] and
                'description' in message['data']['incident']['trigger_summary_data']):
            return message['data']['incident']['trigger_summary_data']['description']
        else:
            return None

    def handle_triggered_incident(self, message):
        """
        Handles a new pager duty triggered alert.
        """
        # Find out who this was assigned to
        names = ', '.join([
            assigned_to['object']['name']
            for assigned_to in message['data']['incident']['assigned_to']
        ])
        client = self.get_client_from_message(message)
        description = self.get_description_from_message(message)

        # Build fields for the custom message attachment
        custom_message_fields = [{
            'title': 'Assigned To',
            'value': names,
            'short': True
        }]
        if client:
            custom_message_fields.append({
                'title': 'Client',
                'value': client,
                'short': True
            })

        trigger_style = [{
            'fallback': 'pagerduty alert',
            'color': '#c52929',
            'fields': custom_message_fields,
        }]
        t_style = json.dumps(trigger_style)

        message = '{0} (<{1}|Incident details> | <{2}|Trigger details>)'.format(
            description, message['data']['incident']['html_url'],
            message['data']['incident']['trigger_details_html_url'])

        slack.chat.post_message('#support', message, attachments=t_style, username='pagerduty', icon_url=self.ICON)

    def handle_resolved_incident(self, message):
        """
        Handles a resolved pager duty alert.
        """
        resolved_by = None
        if message['data']['incident'].get('resolved_by_user'):
            resolved_by = message['data']['incident']['resolved_by_user'].get('name')
        client = self.get_client_from_message(message)
        description = self.get_description_from_message(message)

        # Build fields for the custom message attachment
        custom_message_fields = []
        if resolved_by:
            custom_message_fields.append({
                'title': 'Resolved By',
                'value': resolved_by,
                'short': True
            })
        if client:
            custom_message_fields.append({
                'title': 'Client',
                'value': client,
                'short': True
            })

        message = '*Resolved* {0} (<{1}|Incident details> | <{2}|Trigger details>)'.format(
            description, message['data']['incident']['html_url'],
            message['data']['incident']['trigger_details_html_url'])

        resolve_style = [{
            'fallback': 'pagerduty alert',
            'color': '228b22',
            'fields': custom_message_fields
        }]
        r_style = json.dumps(resolve_style)
        slack.chat.post_message('#support', message, attachments=r_style, username='pagerduty', icon_url=self.ICON)

    def post(self, request, *args, **kwargs):
        """
        Handles webhook posts from Pagerduty
        """
        payload = json.loads(request.body)

        for message in payload['messages']:
            alert_type = message['type']
            incident_uid = message['data']['incident']['id']
            if not AlertReceipt.objects.create_alert_receipt(alert_type, incident_uid):
                # We have already had an alert of this posted to slack, so ignore it
                continue

            if alert_type == 'incident.trigger':
                self.handle_triggered_incident(message)
            elif alert_type == 'incident.resolve':
                self.handle_resolved_incident(message)

        return HttpResponse()
