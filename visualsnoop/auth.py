import time
import base64
import datetime
import hmac
from hashlib import sha1
from wsgiref.handlers import format_date_time

import six
from requests.auth import AuthBase

if six.PY2:
    from urlparse import urlsplit
else:
    from urllib.parse import urlsplit

from visualsnoop import __version__


class VisualSnoopHMACAuth(AuthBase):
    """Attaches VisualSnoop specific HTTP HMAC Authentication to the given Request object.

    :param public_key: Public key generated for a collection on VisualSnoop Keys page.
    :param secret_key: Secret key associated with the public key.
    """

    AUTH_TYPE = 'VSHMAC'

    def __init__(self, public_key, secret_key):
        self.auth_type = self.AUTH_TYPE
        self.client_version = __version__
        self.public_key = public_key
        self.secret_key = secret_key

    def __call__(self, request):
        # Generate RFC 1123 date format
        if not 'Date' in request.headers:
            request.headers['Date'] = format_date_time(
                time.mktime(datetime.datetime.now().timetuple())
            )

        # Add client_version header
        if self.client_version:
            request.headers['X-Visualsnoop-Client-Version'] = self.client_version

        # Split the URL
        scheme, netloc, path, query_string, fragment = urlsplit(request.url)

        # Generate the authentication signature
        signature = base64.encodestring(
            hmac.new(
                self.secret_key.strip().encode('utf-8'),
                '\n'.join([request.method, path, request.headers['Date']]).encode('utf-8'),
                sha1
            ).digest()
        ).strip().decode('utf-8')

        # Add the Authorization header
        request.headers['Authorization'] = '{} {}:{}'.format(
            self.auth_type,
            self.public_key,
            signature
        )

        return request
