from django.urls import path

from . import views

app_name = "ticketing"

urlpatterns = [
    path("", views.renders, name="form"),
    path("vm_provision", views.vm_provision, name="vm_provision"),
    path("vm_deletion", views.vm_deletion, name="vm_deletion"),
    path("launch_vm", views.launch_vm, name="launch_vm"),
    path("lxc_provision", views.lxc_provision, name="lxc_provision"),
    path("lxc_deletion", views.lxc_deletion, name="lxc_deletion"),
    path("launch_lxc", views.launch_lxc, name="launch_lxc"),
]