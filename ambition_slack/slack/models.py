from django.db import models


class SlackUser(models.Model):
    email = models.TextField(unique=True)
    username = models.TextField(unique=True)
    name = models.TextField()

    def __unicode__(self):
        return self.email
