"""
Utils
"""

from datetime import datetime, timedelta
from typing import Tuple

import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import JWTToken, TokenType

User = get_user_model()


def create_token(
    user: "User", ttl: int, secret_key: str, token_type: TokenType, algorithm: str
) -> Tuple[str, datetime]:
    """Create a token"""

    now = timezone.now()
    expires_at = now + timedelta(seconds=ttl)

    jwt_token = jwt.encode(
        {
            "username": user.username,
            "iat": int(now.strftime("%s")),
            "exp": int(expires_at.strftime("%s")),
        },
        secret_key,
        algorithm=algorithm,
    )

    JWTToken.objects.create(
        user=user, token=jwt_token, expires_at=expires_at, type=token_type
    )
    return jwt_token, expires_at
