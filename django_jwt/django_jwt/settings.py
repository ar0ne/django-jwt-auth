from django.conf import settings

if not hasattr(settings, "JWT_SECRET_KEY"):
    settings.JWT_SECRET_KEY = "change-me"

if not hasattr(settings, "JWT_ACCESS_TOKEN_TTL" ):
    settings.JWT_ACCESS_TOKEN_TTL = 1200

if not hasattr(settings, "JWT_REFRESH_TOKEN_TTL"):
    settings.JWT_REFRESH_TOKEN_TTL = 7200

if not hasattr(settings, "JWT_ALGORITHM"):
    # could be "HS256" | "HS384" | "HS512"
    settings.JWT_ALGORITHM = "HS256"
