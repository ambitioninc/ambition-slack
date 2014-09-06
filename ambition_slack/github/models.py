from django.db import models

from ambition_slack.slack.models import SlackUser


class GithubUser(models.Model):
    slack_user = models.OneToOneField(SlackUser)
    username = models.TextField(unique=True)

    def __unicode__(self):
        return self.username
