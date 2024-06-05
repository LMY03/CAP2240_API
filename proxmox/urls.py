from django.urls import path

from . import views

app_name = "proxmox"

urlpatterns = [
    path("", views.renders, name="form"),
    path("success", views.success, name="success"),
    path("clone_vm", views.clone_vm, name="clone_vm"),
    path("delete_vm", views.delete_vm, name="delete_vm"),
]