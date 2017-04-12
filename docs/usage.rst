=====
Usage
=====

To use Django Instagram photo api in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_instagram_photo_api.apps.DjangoInstagramPhotoApiConfig',
        ...
    )

Add Django Instagram photo api's URL patterns:

.. code-block:: python

    from django_instagram_photo_api import urls as django_instagram_photo_api_urls


    urlpatterns = [
        ...
        url(r'^', include(django_instagram_photo_api_urls)),
        ...
    ]
