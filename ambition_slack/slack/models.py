from django.db import models


class SlackUser(models.Model):
    email = models.TextField()
    username = models.TextField()
    name = models.TextField()
