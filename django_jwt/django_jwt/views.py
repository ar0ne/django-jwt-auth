from django.conf import settings
from rest_framework import exceptions, status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from . import messages
from .models import JWTToken, TokenType
from .utils import create_token


@api_view(["POST"])
@permission_classes([])
def obtain_jwt_token(request):
    if not request.user.is_authenticated:
        raise exceptions.AuthenticationFailed(messages.INVALID_CREDENTIALS_ERR_MSG)
    return build_token_response(request.user)


def build_token_response(user) -> Response:
    access_token, _ = create_token(
        user=user,
        ttl=int(settings.JWT_AUTH_TOKEN_TTL),
        secret_key=settings.JWT_SECRET_KEY,
        token_type=TokenType.ACCESS.value,
        algorithm=settings.JWT_ALGORITHM,
    )

    refresh_token, refresh_token_expires_at = create_token(
        user=user,
        ttl=int(settings.JWT_REFRESH_TOKEN_TTL),
        secret_key=settings.SECRET_KEY,
        token_type=TokenType.REFRESH.value,
        algorithm=settings.JWT_ALGORITHM,
    )

    return Response(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": refresh_token_expires_at,
        },
        status=status.HTTP_200_OK,
    )
