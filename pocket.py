import requests
from functools import wraps


class PocketException(Exception):
    '''
    Base class for all pocket exceptions
    http://getpocket.com/developer/docs/errors

    '''
    pass


class InvalidQueryException(PocketException):
    pass


class AuthException(PocketException):
    pass


class RateLimitException(PocketException):
    '''
    http://getpocket.com/developer/docs/rate-limits

    '''
    pass


class ServerMaintenanceException(PocketException):
    pass

EXCEPTIONS = {
    400: InvalidQueryException,
    401: AuthException,
    403: RateLimitException,
    503: ServerMaintenanceException,
}


def method_wrapper(fn):

    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        url = self.api_endpoints[fn.__name__]
        payload = dict([(k, v) for k, v in kwargs.iteritems() if v is not None])
        payload.update(self._payload)

        return self._make_request(url, payload)

    return wrapped


def bulk_wrapper(fn):

    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        wait = kwargs.pop('wait')

        if wait:
            query = dict(
                [(k, v) for k, v in kwargs.iteritems() if v is not None]
            )
            self._bulk_query.append(query)

            return self
        else:
            url = self.api_endpoints['send']
            query = [kwargs]
            payload = {
                'actions': query,
            }

            return self._make_request(url, payload)

    return wrapped


class Pocket(object):
    '''
    This class implements a basic python wrapper around the pocket api. For a
    detailed documentation of the methods and what they do please refer the
    official pocket api documentation at http://getpocket.com/developer/docs/overview

    '''
    def __init__(self, consumer_key, access_token):
        self.consumer_key = consumer_key
        self.access_token = access_token
        self._bulk_query = []

        self._payload = {
            'consumer_key': self.consumer_key,
            'access_token': self.access_token,
        }

        self.api_endpoints = dict(
            (method, 'https://getpocket.com/v3/%s' % method)
            for method in "add,send,get".split(",")
        )

        self.statuses = {
            200: 'Request was successful',
            400: 'Invalid request, please make sure you follow the '
                 'documentation for proper syntax',
            401: 'Problem authenticating the user',
            403: 'User was authenticated, but access denied due to lack of '
                 'permission or rate limiting',
            503: 'Pocket\'s sync server is down for scheduled maintenance.',
        }

    def _make_request(self, url, payload, headers=None):
        r = requests.post(url, data=payload, headers=headers)

        if r.status_code > 399:
            error_msg = self.statuses.get(r.status_code)
            extra_info = r.headers.get('X-Error')
            raise EXCEPTIONS.get(r.status_code, PocketException)(
                '%s %s' % (error_msg, extra_info)
            )

        return r.json() or r.text, r.headers

    @method_wrapper
    def add(self, url, title=None, tags=None, tweet_id=None):
        '''
        This method allows you to add a page to a user's list.
        In order to use the /v3/add endpoint, your consumer key must have the
        "Add" permission.
        http://getpocket.com/developer/docs/v3/add

        '''

    @method_wrapper
    def get(
        self, state=None, favorite=None, tag=None, contentType=None,
        sort=None, detailType=None, search=None, domain=None, since=None,
        count=None, offset=None
    ):
        '''
        This method allows you to retrieve a user's list. It supports
        retrieving items changed since a specific time to allow for syncing.
        http://getpocket.com/developer/docs/v3/retrieve

        '''

    @method_wrapper
    def send(self, actions):
        '''
        This method allows you to make changes to a user's list. It supports
        adding new pages, marking pages as read, changing titles, or updating
        tags. Multiple changes to items can be made in one request.
        http://getpocket.com/developer/docs/v3/modify

        '''

    @bulk_wrapper
    def bulk_add(
        self, item_id, ref_id=None, tags=None, time=None, title=None,
        url=None, wait=True
    ):
        pass

    @bulk_wrapper
    def archive(self, item_id, time=None):
        pass

    def commit(self):
        '''
        This method executes the bulk query, flushes stored queries and
        returns the response

        '''
        url = self.api_endpoints['send']
        payload = {
            'actions': self._bulk_query,
        }

        return self._make_request(url, payload)

    @staticmethod
    def auth(consumer_key, redirect_uri='http://example.com/', state=None):
        '''
        OAUTH2 authentication for getting the access token
        http://getpocket.com/developer/docs/authentication

        '''
        headers = {
            'X-Accept': 'application/json',
        }
        url = 'https://getpocket.com/v3/oauth/request'
        data = {
            'consumer_key': consumer_key,
            'redirect_uri': redirect_uri,
        }

        if state:
            data['state'] = state

        r = requests.post(url, data=data, headers=headers)
        code = r.json()['code']

        auth_url = 'https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s' % (code, redirect_uri)
        raw_input('Please open %s in your browser to authorize the app and press enter:' % auth_url)

        url2 = 'https://getpocket.com/v3/oauth/authorize'
        data2 = {
            'consumer_key': consumer_key,
            'code': code,
        }
        r2 = requests.post(url2, data=data2, headers=headers)
        return r2.json()['access_token']
