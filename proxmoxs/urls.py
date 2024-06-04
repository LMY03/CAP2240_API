from django.urls import path

from . import views

app_name = "proxmoxs"
urlpatterns = {
    path("", views.form),
}