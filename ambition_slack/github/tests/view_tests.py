import json

from django.test import TestCase
from django.test.client import Client
from django_dynamic_fixture import G, F
from mock import patch

from ambition_slack.github.models import GithubUser
from ambition_slack.github.payload import GithubPayload
from ambition_slack.github.views import GithubView


class TestGithubViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_githubview(self):
        response = self.client.get('/github/')
        self.assertEqual(response.status_code, 200)

    def test_githubview_git(self):
        response = self.client.get('/github/')
        self.assertEqual(response.content, 'Github')

    def test_handle_pull_request_repo_action_no_call(self):
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        payload = {'sender': {'login': 'jodything'},
                   'pull_request': {'assignee': {'login': 'jodything'}},
                   'action': None}
        self.assertFalse(None, GithubView().handle_pull_request_repo_action(GithubPayload(payload)))

    @patch('ambition_slack.github.views.slack', spec_set=True)
    def test_post_pull_request_action_opened_assigned(self, slack):
        # Setup the scenario
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        G(
            GithubUser, username='test_user',
            slack_user=F(username='test_slackuser'))
        pr_url = 'http://github.com/pretend/pr'
        # construct a payload as a dictionary
        payload = {
            'pull_request': {
                'assignee': {'login': 'test_user', },
                'body': '',
                'html_url': pr_url, },
            'action': 'opened',
            'sender': {'login': 'jodything'},
        }
        # create a client
        # post the payload json to the client
        self.client.post(
            '/github/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '@test_slackuser',
            'Pull request opened by Jody - ({})'.format(pr_url, username='github'),
            username='github')

    @patch('ambition_slack.github.views.slack', spec_set=True)
    def test_post_pull_request_action_opened_pr_body(self, slack):
        # Setup the scenario
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        G(
            GithubUser, username='test_user',
            slack_user=F(username='test_slackuser'))
        pr_url = 'http://github.com/pretend/pr'
        # construct a payload as a dictionary
        payload = {
            'pull_request': {
                'assignee': None,
                'body': '@jodything',
                'html_url': pr_url, },
            'action': 'opened',
            'sender': {'login': 'jodything'}, }
        # create a client & post the payload json to the client
        self.client.post(
            '/github/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '@jody_slackuser',
            'Pull request opened by Jody - ({})'.format(pr_url, username='github'),
            username='github')

    @patch('ambition_slack.github.views.slack', spec_set=True)
    def test_post_pull_request_comment_action(self, slack):
        # Setup the scenario
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        G(
            GithubUser, username='test_user',
            slack_user=F(username='test_slackuser'))
        pr_url = 'http://github.com/pretend/pr'
        # construct a payload as a dictionary
        payload = {'issue': {'pull_request': {'html_url': pr_url, }, },
                   'action': 'created',
                   'comment': {'body': '@test_user', },
                   'sender': {'login': 'jodything', }, }
        # create a client & post the payload json to the client
        self.client.post(
            '/github/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '@test_slackuser',
            'Pull request comment from Jody - ({})'.format(pr_url, username='github'),
            username='github')

    @patch('ambition_slack.github.views.slack', spec_set=True)
    def test_post_pull_request_action_merged(self, slack):
        # Setup the scenario
        pr_url = 'http://github.com/pretend/pr'
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        # construct a payload as a dictionary
        payload = {
            'pull_request': {
                'merged': '',
                'assignee': None,
                'body': '@jodything',
                'html_url': pr_url, },
            'action': 'closed',
            'sender': {'login': 'jodything'},
        }
        # create a client & post the payload json to the client
        self.client.post(
            '/github/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '@jody_slackuser',
            'Pull request closed by Jody - ({})'.format(pr_url, username='github'),
            username='github')

    @patch('ambition_slack.github.views.slack', spec_set=True)
    def test_post_pull_request_action_opened_w_assignee(self, slack):
        # Setup the scenario
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        G(
            GithubUser, username='test_user',
            slack_user=F(username='test_slackuser'))
        pr_url = 'http://github.com/pretend/pr'
        # construct a payload as a dictionary
        payload = {
            'pull_request': {
                'assignee': {'login': 'test_user', },
                'body': '@test_slackuser',
                'html_url': pr_url, },
            'action': 'assigned',
            'sender': {'login': 'jodything'}, }
        # create a client & post the payload json to the client
        self.client.post(
            '/github/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '@test_slackuser',
            'Pull request assigned to you by Jody - ({})'.format(pr_url, username='github'),
            username='github')

    @patch('ambition_slack.github.views.slack', spec_set=True)
    def test_post_pull_request_action_assigned(self, slack):
        # Setup the scenario
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        G(
            GithubUser, username='test_user',
            slack_user=F(username='test_slackuser'))
        # construct a payload as a dictionary
        payload = {'action': 'assigned',
                   'sender': {'login': 'jodything'}, }
        # create a client
        # post the payload json to the client
        self.client.post(
            '/github/', json.dumps(payload),
            content_type='application/json')
        # Verify that slack posts a message
        self.assertFalse(slack.chat.post_message.called)
