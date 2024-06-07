from django.urls import path

from . import views

app_name = "ticketing"

urlpatterns = [
    path("", views.renders, name="form"),
    path("vm_provision", views.vm_provision, name="vm_provision"),
]