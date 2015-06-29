from requests import get as r_get
from pprint import pprint
from simplejson import JSONDecodeError
from requests.exceptions import ConnectionError, Timeout, SSLError

from tintin.errors import GenericError
from tintin.models import BaseDTO


# BaseJSONApi?
class BaseApi(object):
    def __init__(self, endpoint=None, username=None, password=None, defaults=None):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.defaults = defaults

    def request(self, method, debug=False, api_format='json', **kwargs):
        url = self.endpoint.format(method)
        params = kwargs

        to_pass = []
        for k, v in params.iteritems():
            if v is None:
                to_pass.append(k)
        for p in to_pass:
            del params[p]

        if self.defaults:
            params.update(self.defaults)

        try:
            response = r_get(url, auth=(self.username, self.password), params=params)
        except (ConnectionError, Timeout, SSLError):
            raise GenericError

        if api_format == 'json':
            try:
                output = response.json()
            except JSONDecodeError:
                output = response.content
        else:
            output = response.content

        if debug:
            pprint(output)
        return output


class BaseCursorDataIterator(object):
    def __init__(self, request_func, method, rows=None, **kwargs):
        self.request_func = request_func
        self.method = method
        self.rows = rows
        self.data = None
        self.cursor = 0
        self.offset = 0
        self.kwargs = kwargs

    def __iter__(self):
        return self

    def next(self):
        current = None
        if not self.data:
            self.data = self.request_func(self.method, **self.kwargs)
        data_len = len(self.data) if self.data else 0
        if self.cursor < data_len:
            current = self.data[self.cursor]
            self.cursor += 1
            if self.cursor == data_len == self.rows:
                self.offset = self.offset + self.rows
                self.cursor = 0
                self.data = self.request_func(self.method, rows=self.rows, offset=self.offset, **self.kwargs)
            return BaseDTO(current)
        else:
            self.offset = 0
            self.cursor = 0
            raise StopIteration()
