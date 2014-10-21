from django.db import models, IntegrityError

from ambition_slack.slack.models import SlackUser


class PagerdutyUser(models.Model):
    slack_user = models.OneToOneField(SlackUser)
    email = models.TextField(unique=True)

    def __unicode__(self):
        return self.email


class AlertReceiptManager(models.Manager):
    def create_alert_receipt(self, alert_type, incident_uid):
        """
        Creates a new alert receipt if it doesn't exist and returns it. Returns None if
        the receipt already exists.
        """
        try:
            return self.create(alert_type=alert_type, incident_uid=incident_uid)
        except IntegrityError:
            return None


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

    objects = AlertReceiptManager()

    class Meta:
        unique_together = ('alert_type', 'incident_uid')
