from django.core.exceptions import ImproperlyConfigured

try:
    from django_jwt import settings  # noqa: F401
except ImproperlyConfigured:
    pass

