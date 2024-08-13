from django.conf import settings
from rest_framework import exceptions, status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import messages
from .models import JWTToken, TokenType
from .utils import create_token
from rest_framework.exceptions import ValidationError
from django.utils import timezone


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_me(request):
    return Response(data={"message": "Hooray! You successfully passed JWT authentication!"})


@api_view(["POST"])
@permission_classes([])
def obtain_jwt_token(request) -> Response:
    if not request.user.is_authenticated:
        raise exceptions.AuthenticationFailed(messages.INVALID_CREDENTIALS_ERR_MSG)
    return build_token_response(request.user)


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def refresh_jwt_token(request) -> Response:
    if not (refresh_token := request.data.get("refresh_token")):
        raise ValidationError(detail={"refresh_token": messages.REQUIRED_FIELD_ERR_MSG})

    try:
        token = JWTToken.objects.get(token=refresh_token, type=TokenType.REFRESH.value)
    except JWTToken.DoesNotExist:
        raise ValidationError(detail={"refresh_token": messages.TOKEN_IS_NOT_EXIST_IN_DATABASE})
   
    if token.expires_at > timezone.now():
        user = token.user
        return build_token_response(user)
    
    raise exceptions.AuthenticationFailed(messages.TOKEN_EXPIRED_ERR_MSG)

def build_token_response(user) -> Response:
    access_token, _ = create_token(
        user=user,
        ttl=int(settings.JWT_ACCESS_TOKEN_TTL),
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


