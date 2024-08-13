from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from .models import JWTToken


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        token_key = scope["query_string"].decode().split("=")[-1]
        scope["user"] = await self.get_user(token_key)
        return await super().__call__(scope, receive, send)

    @staticmethod
    @database_sync_to_async
    def get_user(token_key):
        try:
            token = JWTToken.objects.get(token=token_key)
            return token.user
        except JWTToken.DoesNotExist:
            return AnonymousUser()
