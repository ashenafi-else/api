===
Api
===

Api is a application of else platform.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "api" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'api',
    ]

2. Include the common URLconf in your project urls.py like this::

    path('', include('api.urls')),

3. Run `python manage.py migrate` to create the api models.

4. Visit http://127.0.0.1:8000/api to participate in the api.
