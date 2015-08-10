class GithubPayload(object):
    """
    This class provides a wrapper around the Github API posts.
    """
    def __init__(self, message_dict):
        self.message_dict = message_dict

    @property
    def action(self):
        return self.message_dict['action']

    @property
    def assignee_login(self):
        try:
            return self.message_dict['pull_request']['assignee'].get('login')
        except (KeyError, AttributeError):
            return None

    @property
    def sender_login(self):
        try:
            return self.message_dict['sender']['login']
        except KeyError:
            return None

    @property
    def is_pull_request_action(self):
        return self.is_repo_action and self.is_pull_request

    @property
    def is_pull_request_comment(self):
        return self.is_issue and self.action == 'created'

    @property
    def is_closed(self):
        return self.action == 'closed'

    @property
    def is_assigned(self):
        return self.action == 'assigned'

    @property
    def is_opened_or_merged(self):
        return self.action in ['opened', 'closed', 'merged']

    @property
    def is_repo_action(self):
        return self.is_opened_or_merged or self.is_assigned or self.is_closed

    @property
    def is_issue(self):
        return 'issue' in self.message_dict

    @property
    def is_pull_request(self):
        return 'pull_request' in self.message_dict

    @property
    def pull_request_html_url(self):
        try:
            return self.message_dict['pull_request']['html_url']
        except KeyError:
            return None

    @property
    def pull_request_comment(self):
        try:
            return self.message_dict['issue']['pull_request']['html_url']
        except KeyError:
            return None

    @property
    def pull_request_body(self):
        try:
            return self.message_dict['pull_request']['body']
        except KeyError:
            return None

    @property
    def comment_body(self):
        try:
            return self.message_dict['comment']['body']
        except KeyError:
            return None

    def mentions_user(self, github_username):
        """
        Determine if the specified github_username is mentioned in the pull request.
        """
        mention_string = '@{0}'.format(github_username)

        if self.pull_request_body and mention_string in self.pull_request_body:
            return True

        if self.comment_body and mention_string in self.comment_body:
            return True

        return False
