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


class PagerdutyMessage(object):
    """
    This class provides a wrapper around the PagerDuty API message.
    """
    def __init__(self, message_dict):
        self.message_dict = message_dict

    @property
    def incident_id(self):
        return self.message_dict['data']['incident']['id']

    @property
    def alert_type(self):
        return self.message_dict['type']

    @property
    def client(self):
        try:
            return self.message_dict['data']['incident']['trigger_summary_data']['client']
        except KeyError:
            return None

    @property
    def description(self):
        try:
            return self.message_dict['data']['incident']['trigger_summary_data']['description']
        except KeyError:
            return None

    @property
    def resolved_by(self):
        try:
            return self.message_dict['data']['incident']['resolved_by_user'].get('name')
        except KeyError:
            return None

    @property
    def incidient_html_url(self):
        try:
            return self.message_dict['data']['incident']['html_url']
        except KeyError:
            return None

    @property
    def incidient_trigger_details_html_url(self):
        try:
            return self.message_dict['data']['incident']['trigger_details_html_url']
        except KeyError:
            return None

    @property
    def assigned_to_list(self):
        return [
            assigned_to['object']['name']
            for assigned_to in self.message_dict['data']['incident']['assigned_to']
        ]


class PagerdutyView(View):
    ICON = 'https://pbs.twimg.com/profile_images/482648331181490177/4X_QI2Vu_400x400.png'

    def get(self, *args, **kwargs):
        return HttpResponse('Pagerduty')

    def handle_triggered_incident(self, pd_message):
        """
        Handles a new pager duty triggered alert.
        """
        # Build fields for the custom message attachment
        custom_message_fields = []
        self._attached_assigned_to_message_field(pd_message, custom_message_fields)
        self._attach_client_message_field(pd_message, custom_message_fields)

        trigger_style = [{
            'fallback': 'pagerduty alert',
            'color': '#c52929',
            'fields': custom_message_fields,
        }]
        t_style = json.dumps(trigger_style)

        message = '{0} (<{1}|Incident details> | <{2}|Trigger details>)'.format(
            pd_message.description, pd_message.incidient_html_url,
            pd_message.incidient_trigger_details_html_url)

        slack.chat.post_message('#support', message, attachments=t_style, username='pagerduty', icon_url=self.ICON)

    def handle_resolved_incident(self, pd_message):
        """
        Handles a resolved pager duty alert.
        """
        # Build fields for the custom message attachment
        custom_message_fields = []
        self._attach_resolved_by_message_field(pd_message, custom_message_fields)
        self._attach_client_message_field(pd_message, custom_message_fields)

        message = '*Resolved* {0} (<{1}|Incident details> | <{2}|Trigger details>)'.format(
            pd_message.description, pd_message.incidient_html_url,
            pd_message.incidient_trigger_details_html_url)

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
            pd_message = PagerdutyMessage(message)
            if not AlertReceipt.objects.create_alert_receipt(pd_message.alert_type, pd_message.incident_id):
                # We have already had an alert of this posted to slack, so ignore it
                continue

            if pd_message.alert_type == 'incident.trigger':
                self.handle_triggered_incident(pd_message)
            elif pd_message.alert_type == 'incident.resolve':
                self.handle_resolved_incident(pd_message)

        return HttpResponse()

    def _attach_client_message_field(self, pd_message, message_fields):
        if pd_message.client:
            message_fields.append({
                'title': 'Client',
                'value': pd_message.client,
                'short': True
            })
        return message_fields

    def _attach_resolved_by_message_field(self, pd_message, message_fields):
        if pd_message.resolved_by:
            message_fields.append({
                'title': 'Resolved By',
                'value': pd_message.resolved_by,
                'short': True
            })
        return message_fields

    def _attached_assigned_to_message_field(self, pd_message, message_fields):
        message_fields.append({
            'title': 'Assigned To',
            'value': ', '.join(pd_message.assigned_to_list),
            'short': True
        })
        return message_fields
