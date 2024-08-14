from enum import IntEnum
from typing import List, Tuple

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TokenType(IntEnum):
    ACCESS = 1
    REFRESH = 2

    @classmethod
    def choices(cls) -> List[Tuple[str, int]]:
        return [(key.name, key.value) for key in cls]


class JWTToken(models.Model):
    """
    JWT Token Model
    """

    token = models.CharField(max_length=1024, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jwt_tokens")
    expires_at = models.DateTimeField(null=False, blank=False)
    type = models.IntegerField(choices=TokenType.choices(), default=TokenType.ACCESS)
