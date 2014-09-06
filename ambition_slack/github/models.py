from django.db import models


class GithubUser(models.Model):
    email = models.TextField()
    username = models.TextField()
