from django.urls import path

from . import views

app_name = "jwt_auth"

urlpatterns = [
    path("obtain/", views.obtain_jwt_token, name="obtain_jwt_token"),
    path("refresh/", views.refresh_jwt_token, name="refresh_jwt_token"),
    path("test/", views.test_me, name="test_jwt_auth"),
]
