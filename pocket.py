import requests
import urllib
try:
    import json
except ImportError:
    import simplejson as json

class Pocket:
    def __init__(self, username, password, api_key):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.api_endpoints = {
            'add': 'https://readitlaterlist.com/v2/add',
        }
        self.statuses = {
            200: 'Request was successful',
            400: 'Invalid request, please make sure you follow the documentation for proper syntax',
            401: 'Username and/or password is incorrect',
            403: 'Rate limit exceeded, please wait a little bit before resubmitting',
            503: 'Read It Later\'s sync server is down for scheduled maintenance',
        }

    def _query_builder(self, **kwargs):
        d = {}
        for k, v in kwargs.iteritems():
            if v:
                d[k] = v
        return urllib.urlencode(d)

    def add(self, url, title=None, ref_id=None):
        query = self._query_builder(**{
            'apikey': self.api_key,
            'username': self.username,
            'password': self.password,
            'url': url,
            'title': title,
            'ref_id': ref_id,
        })
        r = requests.get('%s?%s' % (self.api_endpoints['add'], query))
        print r.content
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            if error_msg:
                print r.headers.get('X-Error')
                raise Exception(error_msg)
            else:
                raise Exception(r.headers.get('X-Error'))
