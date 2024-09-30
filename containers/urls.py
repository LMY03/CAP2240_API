from django.urls import path

from . import views

app_name = "containers"

urlpatterns = [
    path("", views.renders, name="form"),
    path("clone_lxc", views.clone_lxc, name="clone_lxc"),
    path("start_lxc", views.start_lxc, name="start_lxc"),
]