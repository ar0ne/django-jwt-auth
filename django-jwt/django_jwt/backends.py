import logging
from datetime import datetime, timezone as dt_timezone
from typing import Tuple

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import authentication, exceptions

from . import messages
from .models import JWTToken, TokenType

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class JWTAuthentication(authentication.BaseAuthentication):
    AUTHENTICATION_HEADER_PREFIX = "BEARER"

    def authenticate_header(self, request) -> str:
        return self.AUTHENTICATION_HEADER_PREFIX

    def authenticate(self, request) -> Tuple["UserModel", str] | None:
        """
        The `authenticate` method is called on every request, regardless of
        whether the endpoint requires authentication.

        `authenticate` has two possible return values:

        1) Returns `None` if we do not wish to authenticate. Usually
        this means we know authentication will fail. An example of
        this is when the request does not include a token in the
        headers.

        2) Returns `(user, token)` - a user/token combination when
        authentication was successful.
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            logger.debug(messages.INVALID_AUTH_HEADER_ERR_MSG)
            raise exceptions.AuthenticationFailed

        prefix: str = auth_header[0].decode("utf-8")
        token: str = auth_header[1].decode("utf-8")

        if prefix.lower() != self.AUTHENTICATION_HEADER_PREFIX.lower():
            # The auth header prefix is not what we expected. Proceed to next auth backend
            logger.debug(
                "Auth header is not of 'Bearer' type - proceed to next auth backend"
            )
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token: str) -> Tuple["UserModel", str]:
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        try:
            JWTToken.objects.get(token=token, type=TokenType.ACCESS.value)
        except JWTToken.DoesNotExist:
            logger.info(
                messages.TOKEN_IS_NOT_EXIST_IN_DATABASE.format(f"****{token[-6:]}")
            )
            raise exceptions.AuthenticationFailed

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except Exception as ex:  # NOQA
            logger.info(messages.FAILED_TO_DECODE_TOKEN_ERR_MSG)
            raise exceptions.AuthenticationFailed

        if self._is_token_expired(payload):
            logger.debug(messages.TOKEN_EXPIRED_ERR_MSG)
            raise exceptions.AuthenticationFailed

        try:
            user = UserModel.objects.get(username=payload["username"])
        except UserModel.DoesNotExist:
            logger.debug(messages.USER_NOT_FOUND_ERR_MSG)
            raise exceptions.AuthenticationFailed

        if not user.is_active:
            logger.debug(messages.USER_DEACTIVATED_ERR_MSG)
            raise exceptions.AuthenticationFailed(messages.LOGIN_IS_INACTIVE)

        logger.info(f"User logged in: {user}")
        return user, token

    @staticmethod
    def _is_token_expired(payload) -> bool:
        if isinstance(payload["exp"], int):
            now = timezone.now()
            expires_at = datetime.fromtimestamp(payload["exp"], tz=dt_timezone.utc)
            return expires_at < now
        return False

