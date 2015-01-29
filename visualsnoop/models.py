import six
import requests

from . import DEFAULT_ENDPOINT
from .auth import VisualSnoopHMACAuth
from .exceptions import VisualSnoopError


class Collection(object):
    """Represents a VisualSnoop Collection identified by ``public_key``.

    :param public_key: Public key generated for a collection on VisualSnoop Keys page.
    :param secret_key: Secret key associated with the public key.
    :param endpoint: Base URL for the API calls. It must be an valid URL including
        protocol, domain and path.
    :param proxies: Python Requests compatible proxies dictionary.
    :param max_retries: The maximum number of retries each connection
        should attempt. Note, this applies only to failed DNS lookups, socket
        connections and connection timeouts, never to requests where data has
        made it to the server. By default, Requests does not retry failed
        connections.
    :type max_retries: int
    """

    def __init__(self, public_key, secret_key, endpoint=DEFAULT_ENDPOINT,
                 proxies=None, max_retries=2):
        self.endpoint = endpoint.rstrip('/')
        self.session = requests.Session()
        self.session.proxies = proxies
        self.session.auth = VisualSnoopHMACAuth(public_key, secret_key)
        self.session.mount(self.endpoint, requests.adapters.HTTPAdapter(max_retries=max_retries))
        collection = self._get_collection(params={'session': 'init'})
        if not collection:
            raise VisualSnoopError('Unable to get Collection ID')
        if not 'collection_id' in collection:
            raise VisualSnoopError(collection.get('message', 'Unable to get Collection ID'))

        self.id = collection['collection_id']
        self.name = collection.get('collection_name', '')
        self.user = collection.get('user', '')

    def _get_collection(self, params=None, timeout=None):
        url = '{}/collection'.format(self.endpoint)
        response = self.session.get(url, timeout=timeout, params=params)
        return response.json()

    def get_image(self, image_id, timeout=None):
        """Retrieve information about indexed image with ``image_id``.

        :param image_id: ID of an image previously added to the collection.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a Python Requests timeout tuple.
        :type timeout: float or tuple
        """

        url = '{}/image/{}'.format(self.endpoint, image_id)
        response = self.session.get(url, timeout=timeout)
        return response.json()

    def add_image(self, image, image_id=None, update_existing=False, timeout=None):
        """Adds ``image`` to collection, in overwrite-safe manner.

        This method sends image data. Use argument ``image_id`` to specify your own
        ID for the image. If ``image_id`` is ``None`` a unique ID will be generated
        and returned in the response as a value for key ``image_id``. Make sure to
        save the ``image_id`` value from the API response.

        The image with ``image_id`` will not be overwritten if parameter
        ``update_existing`` is False (default). To update an existing image with
        ``image_id``, set ``update_existing`` to True.

        :param image: A file object with image data or a path to a file on filesystem.
        :type image: file or str
        :param image_id: (optional) A unique ID of an image. It will be self generated if omitted.
        :param update_existing: A flag whether to allow overwriting existing images.
        :type update_existing: bool
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a Python Requests timeout tuple.
        :type timeout: float or tuple
        """

        if isinstance(image, six.string_types):
            image = open(image, 'rb')

        url = '{}/image/{}'.format(self.endpoint, image_id)
        if image_id is None:
            url = '{}/image'.format(self.endpoint)

        if update_existing and image_id is not None:
            response = self.session.put(url, data=image, timeout=timeout)
        else:
            response = self.session.post(url, data=image, timeout=timeout)
        return response.json()

    def delete_image(self, image_id, timeout=None):
        """Remove image with ``image_id`` from collection.

        :param image_id: ID of an image previously added to the collection.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a Python Requests timeout tuple.
        :type timeout: float or tuple
        """

        url = '{}/image/{}'.format(self.endpoint, image_id)
        response = self.session.delete(url, timeout=timeout)
        return response.json()

    def search_images_by_id(self, image_id, timeout=None):
        """Perform search over collection based on image within the same collection with ID ``image_id``.

        :param image_id: ID of an image previously added to the collection.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a Python Requests timeout tuple.
        :type timeout: float or tuple
        """

        url = '{}/search/{}'.format(self.endpoint, image_id)
        response = self.session.get(url, timeout=timeout)
        return response.json()

    def search_images(self, image, timeout=None):
        """Perform search over collection based on ``image`` sent in the request body.

        :param image: A file object with image data or a path to a file on filesystem.
        :type image: file or str
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a Python Requests timeout tuple.
        :type timeout: float or tuple
        """

        url = '{}/search'.format(self.endpoint)
        if isinstance(image, six.string_types):
            image = open(image, 'rb')
        response = self.session.post(url, data=image, timeout=timeout)
        return response.json()

    def get_images(self, start=None, count=None, timeout=None):
        """List images in collection sorted by time.

        :param start: Image ID from which to start the listing.
        :param count: Number of images in listing.
        """

        url = '{}/images'.format(self.endpoint)
        params = {'start': start}
        if count:
            params['count'] = count
        response = self.session.get(url, params=params, timeout=timeout)
        return response.json()
