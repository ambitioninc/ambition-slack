import logging

from django.http import HttpResponse
from django.views.generic.base import View


LOG = logging.getLogger('console_logger')


class GithubView(View):
    def post(self, request, *args, **kwargs):
        LOG.info('Post')
        LOG.info(request.__dict__)
        return HttpResponse()
