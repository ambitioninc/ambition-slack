from django.test import TestCase
from mock import patch
import requests

from ambition_slack.github.issue import (
    _build_auth_header, _fetch_issues, fetch_assigned_pull_requests, fetch_pull_requests_with_mention, GithubIssue
)
from ambition_slack.github.models import GithubUser


class GithubIssueTests(TestCase):
    def test_title(self):
        self.assertEquals(
            'a repo - a title',
            GithubIssue({
                'repository': {
                    'name': 'a repo',
                },
                'title': 'a title',
            }).title)

    def test_pull_request_link(self):
        self.assertEquals(
            'www.pr.com',
            GithubIssue({
                'pull_request': {
                    'html_url': 'www.pr.com',
                },
            }).pull_request_link)

    def test_is_pull_request(self):
        self.assertFalse(GithubIssue({}).is_pull_request)


class BuildAuthHeaderTests(TestCase):
    def test_build_auth_header(self):
        github_user = GithubUser(username='billy', api_token='secret')

        self.assertEquals({
            'Authorization': 'Basic YmlsbHk6c2VjcmV0'
        },
            _build_auth_header(github_user))


class FetchIssuesTests(TestCase):
    @patch('ambition_slack.github.issue.LOG', spec_set=True)
    @patch.object(requests, 'get', spec_set=True)
    def test_fetch_issues_handles_error(self, get, log):
        # Setup scenario
        github_user = GithubUser(username='billy', api_token='secret')
        e = Exception()
        get.side_effect = e
        filter_str = 'mentioned'

        # Run code
        self.assertEquals([], _fetch_issues(github_user, filter_str))

        # Verify expectations
        log.error.assert_called_once_with(
            'Cannot fetch issues.  filter: "{0}", exception: "{1}"'.format(filter_str, str(e)))

    @patch.object(requests, 'get', spec_set=True)
    def test_fetch_assigned_pull_requests(self, get):
        # Setup scenario
        github_user = GithubUser(username='billy', api_token='secret')
        get.return_value.json.return_value = [
            {
                'pull_request': {
                    'html_url': 'www.pr.com',
                },
                'repository': {
                    'name': 'a repo',
                },
                'title': 'a title',
            },
            {
                'repository': {
                    'name': 'another repo',
                },
            },
        ]

        # Run code
        issues = fetch_assigned_pull_requests(github_user)

        # Verify expectations
        get.assert_called_once_with('https://api.github.com/issues?filter=assigned', headers={
            'Authorization': 'Basic YmlsbHk6c2VjcmV0'
        })
        self.assertEquals(1, len(issues))
        self.assertEquals('www.pr.com', issues[0].pull_request_link)
        self.assertEquals('a repo - a title', issues[0].title)

    @patch.object(requests, 'get', spec_set=True)
    def test_fetch_pull_requests_with_mention(self, get):
        # Setup scenario
        github_user = GithubUser(username='billy', api_token='secret')
        get.return_value.json.return_value = [
            {
                'pull_request': {
                    'html_url': 'www.pr.com',
                },
                'repository': {
                    'name': 'a repo',
                },
                'title': 'a title',
            },
            {
                'repository': {
                    'name': 'another repo',
                },
            },
        ]

        # Run code
        issues = fetch_pull_requests_with_mention(github_user)

        # Verify expectations
        get.assert_called_once_with('https://api.github.com/issues?filter=mentioned', headers={
            'Authorization': 'Basic YmlsbHk6c2VjcmV0'
        })
        self.assertEquals(1, len(issues))
        self.assertEquals('www.pr.com', issues[0].pull_request_link)
        self.assertEquals('a repo - a title', issues[0].title)
