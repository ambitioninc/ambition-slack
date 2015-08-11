from django.test import TestCase

from ambition_slack.github.payload import GithubPayload


class GithubPayloadTests(TestCase):
    def test_get_assignee(self):
        payload = {
            'pull_request': {
                'assignee': {
                    'login': 'jodything',
                },
            },
        }
        self.assertEqual('jodything', GithubPayload(payload).assignee_login)

    def test_get_assignee_returns_none(self):
        self.assertIsNone(GithubPayload({}).assignee_login)

    def test_get_sender_login(self):
        payload = {
            'sender': {
                'login': 'jodything',
            },
        }
        self.assertEqual('jodything', GithubPayload(payload).sender_login)

    def test_get_sender_login_returns_none(self):
        self.assertIsNone(GithubPayload({}).sender_login)

    def test_mentions_user_when_pull_request_mentions_user(self):
        """
        Verify that we detect when a user is mentioned in the pull request body.
        """
        payload = {
            'pull_request': {
                'body': '@jaredlewis please review',
            },
        }
        self.assertTrue(GithubPayload(payload).mentions_user('jaredlewis'))

    def test_mentions_user_when_comment_mentions_user(self):
        """
        Verify that we detect when a user is mentioned in a comment.
        """
        payload = {
            'comment': {
                'body': '@jaredlewis please review',
            },
        }
        self.assertTrue(GithubPayload(payload).mentions_user('jaredlewis'))

    def test_mentions_user_returns_false(self):
        """
        Verify that we detect when a user is not mentioned comment
        """
        payload = {
            'comment': {
                'body': '@jaredlewis please review',
            },
        }
        self.assertFalse(GithubPayload(payload).mentions_user('haha-i-*never*-exist'))

    def test_pull_request_html_url(self):
        payload = {
            'pull_request': {
                'html_url': 'http://if-only-i-existed.com',
            },
        }
        self.assertTrue(payload['pull_request']['html_url'], GithubPayload(payload).pull_request_html_url)

    def test_pull_request_html_url_returns_none(self):
        self.assertIsNone(GithubPayload({}).pull_request_html_url)

    def test_pull_request_comment(self):
        payload = {
            'issue': {
                'pull_request': {
                    'html_url': 'http://if-only-i-existed.com',
                },
            },
        }
        self.assertTrue(payload['issue']['pull_request']['html_url'], GithubPayload(payload).pull_request_comment)

    def test_pull_request_comment_returns_none(self):
        self.assertIsNone(GithubPayload({}).pull_request_comment)
