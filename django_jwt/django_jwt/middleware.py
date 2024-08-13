import logging
from django.contrib.auth.models import AnonymousUser

from .models import JWTToken

logger = logging.getLogger(__name__)

def get_user(token_key):
    try:
        token = JWTToken.objects.get(token=token_key)
        return token.user
    except JWTToken.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, get_response):
        # Store the ASGI application we were passed
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers['authorization'].split()[-1]
        request.scope['user'] = get_user(token)
        return self.get_response(request)

