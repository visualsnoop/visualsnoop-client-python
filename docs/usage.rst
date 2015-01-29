.. _usage:

Usage
=====

Register an account on `VisualSnoop.com <http://visualsnoop.com/>`_, create a collection and prepare ``public`` and ``secret`` keys.

Connecting
----------

Import ``visualsnoop.models.Collection``::

    >>> from visualsnoop.models import Collection

Initialize a session to interact with that collection using API access keys::

    >>> collection = Collection(public_key='24d337fe0ed9427cb512', secret_key='sUGSL96ZvNxqHixSPUopX5L1MtSPdkjrSPrPOCMX')

.. note::

    Values in this example are not valid. Use keys for your own collection.

To verify collection attributes, check properties ``id``, ``name`` and/or ``user``::

    >>> collection.id
    '6b7c9142'
    >>> collection.name
    'Example collection'
    >>> collection.user
    'user@example.com'

Adding images to collection
---------------------------

Adding a new image to the collection::

    >>> collection.add_image(image='example1.jpg')
    {
        'image_time': '2015-01-25T20:43:05.690218+00:00',
        'collection_id': '6b7c9142',
        'image_id': 'c14d4bae93a95c159360e29de998181b',
        'message': 'Added',
        'status': 201
    }

Make sure to save the ``image_id`` value as it is the reference to the actual image. If you want to specify
your own unique ID, for example an ID from your local database provide it within the call::

    >>> collection.add_image(image='example2.jpg', image_id='myid12')
    {
        'image_time': '2015-01-25T20:47:10.021689+00:00',
        'collection_id': '6b7c9142',
        'image_id': 'myid12',
        'message': 'Added',
        'status': 201
    }


Valid image IDs are any strings up to 100 characters long, but integers are most often used for referencing.

In case that you want to update your image with a fresh data, set update_existing to True::

    >>> collection.add_image(image='example3.jpg', image_id='c14d4bae93a95c159360e29de998181b', update_existing=True)
    {
        'image_time': '2015-01-25T20:50:36.384015+00:00',
        'collection_id': '6b7c9142',
        'image_id': 'c14d4bae93a95c159360e29de998181b',
        'message': 'Updated',
        'status': 200
    }

Argument ``update_existing`` is by default set to False, to prevent accidental image overwriting.

Searching
---------

Searching can be performed in two ways:
    * By ID of the image that is already in collection
    * By sending image data of a local image

::

    >>> collection.search_images_by_id(image_id='c14d4bae93a95c159360e29de998181b')
    {
        'message': 'OK',
        'status': 200,
        'image_time': '2015-01-25T20:50:36.384015+00:00',
        'collection_id': '6b7c9142',
        'results': [],
        'image_id': 'c14d4bae93a95c159360e29de998181b'
    }

    >>> collection.search_images(image='example3.jpg')
    {
        'collection_id': '6b7c9142',
        'results': [{'id': 'c14d4bae93a95c159360e29de998181b', 'rank': 0}],
        'message': 'OK',
        'status': 200
    }

Verifying images by ID
----------------------

    >>> collection.get_image(image_id='myid12')
    {
        'image_time': '2015-01-25T20:47:10.021689+00:00',
        'collection_id': '6b7c9142',
        'image_id': 'myid12',
        'message': 'OK',
        'status': 200
    }
    >>> collection.get_images()
    {
        'collection_id': '6b7c9142',
        'status': 200,
        'message': 'OK',
        'images': [
            {
                'image_time': '2015-01-25T20:50:36.384015+00:00',
                'id': 'c14d4bae93a95c159360e29de998181b'
            },
            {
                'image_time': '2015-01-25T20:47:10.021689+00:00',
                'id': 'myid12'
            }
        ],
        'next_image_id': None
    }

Deleting images by ID
---------------------

    >>> collection.delete_image(image_id='myid12')
    {
        'image_time': '2015-01-25T20:47:10.021689+00:00',
        'collection_id': '6b7c9142',
        'image_id': 'myid12',
        'message': 'Deleted',
        'status': 200
    }


