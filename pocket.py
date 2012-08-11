import requests
from functools import wraps
try:
    import json
except ImportError:
    import simplejson as json

def method_wrapper(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        print 'from wrapper: ', fn.__name__
        print kwargs
        payload = dict([(k, v) for k, v in kwargs.iteritems() if v])
        fn(self, *args, **kwargs)
    return wrapped

class Pocket:
    def __init__(self, username, password, api_key):
        self.username = username
        self.password = password
        self.api_key = api_key
        self._payload = {
            'apikey': self.api_key,
            'username': self.username,
            'password': self.password,
        }
        self.api_endpoints = {
            'add': 'https://readitlaterlist.com/v2/add',
            'send': 'https://readitlaterlist.com/v2/send',
            'get': 'https://readitlaterlist.com/v2/get',
            'stats': 'https://readitlaterlist.com/v2/stats',
            'auth': 'https://readitlaterlist.com/v2/auth',
            'signup': 'https://readitlaterlist.com/v2/signup',
            'api': 'https://readitlaterlist.com/v2/api',
        }
        self.statuses = {
            200: 'Request was successful.',
            400: 'Invalid request, please make sure you follow the documentation for proper syntax.',
            401: 'Username and/or password is incorrect.',
            403: 'Rate limit exceeded, please wait a little bit before resubmitting.',
            503: 'Read It Later\'s sync server is down for scheduled maintenance.',
        }

    def add(self, url, title=None, ref_id=None):
        payload = {
            'url': url,
            'title': title,
            'ref_id': ref_id,
        }
        payload.update(self._payload)
        r = requests.post(self.api_endpoints['add'], data=payload)
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            raise Exception('%s %s' % (error_msg, extra_info))
        print r.content
        return self

    def send(self, url_map=None, read_map=None, update_title=None, update_tags=None):
        pass

    def get_list(self, format, state, myAppOnly, since, count, page, tags):
        pass

    def stats(self, format='json'):
        r = requests.post(self.api_endpoints['stats'], data=self._payload)
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            raise Exception('%s %s' % (error_msg, extra_info))
        return json.loads(r.content)

    def auth(self):
        r = requests.post(self.api_endpoints['auth'], data=self._payload)
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            raise Exception('%s %s' % (error_msg, extra_info))
        print r.content
        return self

    def signup(self):
        r = requests.post(self.api_endpoints['signup'], data=self._payload)
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            raise Exception('%s %s' % (error_msg, extra_info))
        return json.loads(r.content)

    @method_wrapper
    def api(self):
        r = requests.post(self.api_endpoints['api'], data={'apikey': self.api_key})
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            raise Exception('%s %s' % (error_msg, extra_info))
        print r.content
        return r.headers
