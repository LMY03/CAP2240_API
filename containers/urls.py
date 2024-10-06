from django.urls import path

from . import views

app_name = "containers"

urlpatterns = [
    path("", views.renders, name="form"),
    path("clone_lxc", views.clone_lxc, name="clone_lxc"),
    path("create_test_vm", views.create_test_vm, name="create_test_vm"),
    path("test", views.test, name="test"),
]