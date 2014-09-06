from django.contrib import admin

from ambition_slack.github.models import GithubUser


admin.site.register(GithubUser)
