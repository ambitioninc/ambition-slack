import logging

from django.http import HttpResponse
from django.views.generic.base import View


LOG = logging.getLogger(__name__)


class GithubView(View):
    def get(self, request, *args, **kwargs):
        LOG.info('Github')
        return HttpResponse('Github')

    def post(self, request, *args, **kwargs):
        pass
