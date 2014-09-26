'''
import json

from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django_dynamic_fixture import G, F
from mock import patch

from ambition_slack.pagerduty.models import PagerdutyUser
from ambition_slack.slack.models import SlackUser
from ambition_slack.pagerduty.views import PagerdutyView


class Test_PagerdutyModels(TransactionTestCase):

    """
    Tests various aspects of the github models.
    """
    def test_multiple_pagerduty_per_slack_user_not_allowed(self):
        # Try to create multiple github users for the same slack user
        slack_user = SlackUser.objects.create(
            email='Adam@gothamcity.com', username='batman', name='Adam')
        PagerdutyUser.objects.create(slack_user=slack_user, name='Adam West')
        with self.assertRaises(IntegrityError):
            PagerdutyUser.objects.create(slack_user=slack_user, name='Christian Bale')

    def test_Pagerduty_unicode(self):
        pagerduty_user = PagerdutyUser(name='Adam West')
        self.assertEquals(pagerduty_user.__unicode__(), 'Adam West')


class Test_PagerdutyView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pagerduty_view(self):
        response = self.client.get('/pagerduty/')
        self.assertEqual(response.status_code, 200)

    def test_pagerdutyview_git(self):
        response = self.client.get('/pagerduty/')
        self.assertEqual(response.content, 'Pagerduty')

# ########### Test post ############

    @patch('ambition_slack.pagerduty.views.slack', spec_set=True)
    def test_payload_triggered(self, slack):
        G(
            PagerdutyUser, name='Adam West',
            slack_user=F(username='batman', name='Adam'))
        pd_url = 'https://acme.pagerduty.com/incidents/PIJ90N7'
        payload = {'messages': [
            {'type': 'incident.trigger',
             'data':
                {'incident': {'html_url': pd_url},
                 'assigned_to_user': {'name': 'Adam West'}}}]}
        # create a client & post the payload json to the client
        self.client.post(
            '/pagerduty/', json.dumps(payload),
            content_type='application/json')
        slack.chat.post_message.assert_called_with(
            '#support',
            'New Pagerduty Ticket assigned to Adam. Click the link to examine ({})'.format(
                pd_url, username='pagerduty'),
            username='Pagerduty')

    @patch('ambition_slack.pagerduty.views.slack', spec_set=True)
    def test_payload_resolved(self, slack):
        G(
            PagerdutyUser, name='Adam West',
            slack_user=F(username='batman', name='Adam'))
        pd_url = 'https://acme.pagerduty.com/incidents/PIJ90N7'
        payload = {'messages': [
            {'type': 'incident.resolve',
             'data':
                {'incident': {'html_url': pd_url},
                 'assigned_to_user': {'name': 'Adam West'}}}]}
        # create a client & post the payload json to the client
        self.client.post(
            '/pagerduty/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '#support',
            'Pagerduty Ticket assigned to Adam is now Resolved. Thank you. Click the link to examine ({})'.format(
                pd_url, username='pagerduty'),
            username='Pagerduty')
'''
