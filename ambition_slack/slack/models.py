from django.db import models
from timezone_field import TimeZoneField


class SlackUser(models.Model):
    email = models.TextField(unique=True)
    username = models.TextField(unique=True)
    name = models.TextField()
    time_zone = TimeZoneField(default='US/Eastern')
    expects_morning_digest = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email
