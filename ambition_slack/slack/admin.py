from django.contrib import admin

from ambition_slack.slack.models import SlackUser


admin.site.register(SlackUser)
