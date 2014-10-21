from django.db import models

from ambition_slack.slack.models import SlackUser


class PagerdutyUser(models.Model):
    slack_user = models.OneToOneField(SlackUser)
    email = models.TextField(unique=True)

    def __unicode__(self):
        return self.email


class AlertReceipt(models.Model):
    """
    A receipt that a particular type of alert has happened. This allows us to not send
    duplicate alerts to the chatroom
    """
    alert_type = models.CharField(max_length=128, choices=(
        ('incident.trigger', 'Trigger'),
        ('incident.resolve', 'Resolve'),
    ))
    incident_uid = models.CharField(max_length=128)

    class Meta:
        unique_together = ('alert_type', 'incident_uid')
