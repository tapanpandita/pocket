import requests
from functools import wraps
try:
    import json
except ImportError:
    import simplejson as json

def method_wrapper(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        payload = dict([(k, v) for k, v in kwargs.iteritems() if v == None])
        payload.update(self._payload)
        r = requests.post(self.api_endpoints[fn.__name__], data=payload)
        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            exceptions = {
                400: 'InvalidQuery',
                401: 'Auth',
                403: 'RateLimit',
                503: 'ServerMaintenance',
            }
            ExceptionClass = type('%sException' % exceptions.get(r.status_code, 'Pocket'),
                (Exception, ),
                {}
            )
            raise ExceptionClass('%s %s' % (error_msg, extra_info))
        return r.json or r.text, r.headers
    return wrapped

class Pocket:
    '''
    This class implements a basic python wrapper around the pocket api. For a detailed documentation of the methods and what they do please refer the official pocket api documentation at http://getpocket.com/api/docs
    '''
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
        '''
        This method allows you to add a page to a user's list.
        '''
        pass

    @method_wrapper
    def send(self, url_map=None, read_map=None, update_title=None, update_tags=None):
        '''
        This method allows you to make changes to a user's list. It supports adding new pages, marking pages as read, changing titles, or updating tags. Multiple changes to items can be made in one request.
        '''
        pass

    @method_wrapper
    def get(self, format='json', state=None, myAppOnly=None, since=None, count=None, page=None, tags=None):
        '''
        This method allows you to retrieve a user's list. It supports retrieving items changed since a specific time to allow for syncing.
        '''
        pass

    @method_wrapper
    def stats(self, format='json'):
        '''
        This method returns some information about a user's list.
        '''
        pass

    @method_wrapper
    def auth(self):
        '''
        The authentication method is used to verify a supplied username and password is correct (for example when prompting a user for their credentials for the first time). It does not need to be called before using any methods below.
        '''
        pass

    @method_wrapper
    def signup(self):
        '''
        This method allows you to create a new user account.
        '''
        pass

    @method_wrapper
    def api(self):
        '''
        This method allows you to check your current rate limit status. Calls to this method do not count against the rate limit.
        '''
        pass
