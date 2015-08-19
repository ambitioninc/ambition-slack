from django.db import models

from ambition_slack.slack.models import SlackUser


class GithubUser(models.Model):
    slack_user = models.OneToOneField(SlackUser, related_name='github_user')
    username = models.TextField(unique=True)
    api_token = models.TextField(default='')

    def __unicode__(self):
        return self.username
