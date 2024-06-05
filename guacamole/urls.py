from django.urls import path

from . import views

app_name = "guacamole"

urlpatterns = [
    path("", views.render, name="form"),
    path("success", views.success, name="success"),
    path("create_user", views.create_user, name="create_user"),
]