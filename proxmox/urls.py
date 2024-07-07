from django.urls import path

from . import views

app_name = "proxmox"

urlpatterns = [
    path("", views.renders, name="form"),
    path("clone_vm", views.clone_vm, name="clone_vm"),
    path("start_vm", views.start_vm, name="start_vm"),
    path("shutdown_vm", views.shutdown_vm, name="shutdown_vm"),
    path("delete_vm", views.delete_vm, name="delete_vm"),
    path("stop_vm", views.stop_vm, name="stop_vm"),
    path("status_vm", views.status_vm, name="status_vm"),
    path("ip_vm", views.ip_vm, name="ip_vm"),
    path("config_vm", views.config_vm, name="config_vm"),
]