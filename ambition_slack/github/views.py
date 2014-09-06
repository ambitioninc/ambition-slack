import json
import logging

from django.http import HttpResponse
from django.views.generic.base import View


LOG = logging.getLogger('console_logger')


class GithubView(View):
    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        
        if 'pull_request' in payload:
            LOG.info('New PR opened with body {0}'.format(payload['pull_request']['body']))

        return HttpResponse()
