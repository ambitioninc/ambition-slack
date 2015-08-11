import base64

import requests


class GithubIssue(object):
    def __init__(self, message_dict):
        self.message_dict = message_dict

    @property
    def title(self):
        repo_name = self.message_dict['repository']['name']
        title = self.message_dict['title']

        return '{0} - {1}'.format(repo_name, title)

    @property
    def pull_request_link(self):
        return self.message_dict.get('pull_request', {}).get('html_url')

    @property
    def is_pull_request(self):
        return 'pull_request' in self.message_dict


def _build_auth_header(github_user):
    return {
        'Authorization': 'Basic {0}'.format(
            base64.b64encode('{0}:{1}'.format(github_user.username, github_user.api_token)))
    }


def _fetch_issues(github_user, filter_str):
    api_call = 'https://api.github.com/issues?filter={0}'.format(filter_str)

    return [GithubIssue(issue) for issue in requests.get(api_call, headers=_build_auth_header(github_user)).json()]


def fetch_assigned_pull_requests(github_user):
    return [i for i in _fetch_issues(github_user, 'assigned') if i.is_pull_request]


def fetch_pull_requests_with_mention(github_user):
    return [i for i in _fetch_issues(github_user, 'mentioned') if i.is_pull_request]
