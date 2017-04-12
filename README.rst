=============================
Django Instagram photo api
=============================

.. image:: https://badge.fury.io/py/django-instagram-photo-api.svg
    :target: https://badge.fury.io/py/django-instagram-photo-api

.. image:: https://travis-ci.org/DmytroLitvinov/django-instagram-photo-api.svg?branch=master
    :target: https://travis-ci.org/DmytroLitvinov/django-instagram-photo-api

.. image:: https://codecov.io/gh/DmytroLitvinov/django-instagram-photo-api/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/DmytroLitvinov/django-instagram-photo-api

Get photos from Instagram by hashtags

Documentation
-------------

The full documentation is at https://django-instagram-photo-api.readthedocs.io.

Quickstart
----------

Install Django Instagram photo api::

    pip install django-instagram-photo-api

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_instagram_photo_api',
        ...
    )

Add Django Instagram photo api's URL patterns:

.. code-block:: python

    from django_instagram_photo_api import urls as django_instagram_photo_api_urls


    urlpatterns = [
        ...
        url(r'^instagram_app/', include(django_instagram_photo_api_urls, 
            namespace="instagram-feed")),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
