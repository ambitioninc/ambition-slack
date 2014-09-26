from django.db import models

from ambition_slack.slack.models import SlackUser


class PagerdutyUser(models.Model):
    slack_user = models.OneToOneField(SlackUser)
    email = models.TextField(unique=True)

    def __unicode__(self):
        return self.email
