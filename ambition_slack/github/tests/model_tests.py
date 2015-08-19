from django.db import IntegrityError
from django.test import TransactionTestCase

from ambition_slack.github.models import GithubUser
from ambition_slack.slack.models import SlackUser


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
