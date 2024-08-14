==========
Django-JWT
==========

Django-JWT is Django app that provides support of JWT authentication.


Quick start
-----------

1. Add "django_jwt" to your INSTALLED_APPS settings:

INSTALLED_APPS = [
    ...
    "django_jwt",
]

2. You could include URLconf in your project urls.py:

    path("jwt/, include("django_jwt.urls")),

3. Run `python manage.py migrate` to create models:

4. Start the development server and visit admin page.

5. You could obtain, refresh and test token:

.. code-block:: console

    curl --request POST \
    --url http://localhost:8000/jwt/obtain/ \
    --header "Authorization: Basic <base64-user-and-password"

For authorization used encoded base64 "<username>:<password>" string. I.e. "admin:123" is "YWRtaW46MTIz".

.. code-block:: console

   curl --request POST \
   --url http://localhost:8000/jwt/refresh/ \
   --header "Content-Type: application/json" \
   --data "{"refresh_token": "<refresh-token>"}"

.. code-block:: console

    curl --request GET \
    --url http://localhost:8000/jwt/test \
    --header "Authorization: Bearer <access_token>"


