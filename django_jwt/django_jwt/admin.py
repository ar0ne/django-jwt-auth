from django.contrib import admin

from . import models


@admin.register(models.JWTToken)
class JWTTokenAdmin(admin.ModelAdmin):
    pass
