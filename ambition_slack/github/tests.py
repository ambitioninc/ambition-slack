import json

from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django_dynamic_fixture import G, F
from mock import patch

from ambition_slack.github.models import GithubUser
from ambition_slack.slack.models import SlackUser
from ambition_slack.github.views import GithubView


class GithubViewTest(TestCase):
    def dummy_test(self):
        self.assertTrue(True)


# __________Model tests_______________

class ModelsTest(TransactionTestCase):

    """
    Tests various aspects of the github models.
    """
    def test_multiple_github_per_slack_user_not_allowed(self):
        # Try to create multiple github users for the same slack user
        slack_user = SlackUser.objects.create(
            email='test_email', username='test_username', name='Jody')
        GithubUser.objects.create(slack_user=slack_user, username='jodything')
        with self.assertRaises(IntegrityError):
            GithubUser.objects.create(slack_user=slack_user, username='another_username')

    def test_github_unicode(self):
        github_user = GithubUser(username='test_username')
        self.assertEquals(github_user.__unicode__(), 'test_username')

    def test_slack_unicode(self):
        slack_user = SlackUser(email='test_email')
        self.assertEquals(slack_user.__unicode__(), 'test_email')


# ___________View Tests_______________

class TestGithubViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_githubview(self):
        response = self.client.get('/github/')
        self.assertEqual(response.status_code, 200)

    def test_githubview_git(self):
        response = self.client.get('/github/')
        self.assertEqual(response.content, 'Github')

    def test_no_get_assignee(self):
        payload = {'pull_request': {'assignee': None}}
        self.assertEquals(None, GithubView().get_assignee(payload))

    def test_get_assignee_no_github_user(self):
        payload = {'pull_request': {'assignee': {'login': 'jodything'}}}
        self.assertEqual(None, GithubView().get_assignee(payload))

    def test_get_assignee_w_github_user(self):
        github_user = G(GithubUser, username='jodything')
        payload = {'pull_request': {'assignee': {'login': 'jodything'}}}
        self.assertEqual(github_user, GithubView().get_assignee(payload))

    def test_handle_pull_request_repo_action_no_call(self):
        G(
            GithubUser, username='jodything',
            slack_user=F(username='jody_slackuser', name='Jody'))
        payload = {'sender': {'login': 'jodything'},
                   'pull_request': {'assignee': {'login': 'jodything'}},
                   'action': None}
        self.assertFalse(None, GithubView().handle_pull_request_repo_action(payload))

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
