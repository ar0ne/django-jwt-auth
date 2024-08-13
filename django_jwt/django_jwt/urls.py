from django.urls import re_path

from . import views

app_name = "authentication"

urlpatterns = [
    re_path(r"^obtain_token/$", views.obtain_jwt_token, name="obtain_jwt_token"),
    re_path("^test/$", views.test_me, name="test_endpoint"),
]
