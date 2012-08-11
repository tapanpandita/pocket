import requests
from functools import wraps
try:
    import json
except ImportError:
    import simplejson as json

def method_wrapper(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        payload = dict([(k, v) for k, v in kwargs.iteritems() if v])
        payload.update(self._payload)
        r = requests.post(self.api_endpoints[fn.__name__], data=payload)
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            ExceptionClass = type('%sException' % fn.__name__.capitalize(),
                (Exception, ),
                {}
            )
            raise ExceptionClass('%s %s' % (error_msg, extra_info))
        return r.json or r.text, r.headers
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

    @method_wrapper
    def add(self, url, title=None, ref_id=None):
        pass

    def send(self, url_map=None, read_map=None, update_title=None, update_tags=None):
        pass

    def get(self, format, state, myAppOnly, since, count, page, tags):
        pass

    @method_wrapper
    def stats(self, format='json'):
        pass

    @method_wrapper
    def auth(self):
        pass

    @method_wrapper
    def signup(self):
        pass

    @method_wrapper
    def api(self):
        pass
