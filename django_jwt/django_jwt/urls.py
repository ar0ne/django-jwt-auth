from django.conf.urls import url

from . import views

app_name = "authentication"

urlpatterns = [
    url(r"^obtain_token/$", views.obtain_jwt_token, name="obtain_jwt_token"),
]
