from django.urls import path

from . import views

app_name = "proxmox"
urlpatterns = [
    path("", views.render, name="form"),
    path("submit", views.success, name="success"),
    path("submit", views.clone_vm, name="clone_vm"),
]