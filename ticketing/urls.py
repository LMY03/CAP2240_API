from django.urls import path

from . import views

app_name = "ticketing"

urlpatterns = [
    path("", views.renders, name="form"),
    path("vm_provision", views.vm_provision, name="vm_provision"),
    path("vm_deletion", views.vm_deletion, name="vm_deletion"),
    path("launch_vm", views.launch_vm, name="launch_vm"),
]