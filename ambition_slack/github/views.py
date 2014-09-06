import logging

from django.http import HttpResponse
from django.views.generic.base import View


LOG = logging.getLogger('console_logger')


class GithubView(View):
    def get(self, request, *args, **kwargs):
        LOG.info('Github')
        return HttpResponse('Github')

    def post(self, request, *args, **kwargs):
        LOG.info(request.__dict__)
        return super(GithubView, self).post(request, *args, **kwargs)
