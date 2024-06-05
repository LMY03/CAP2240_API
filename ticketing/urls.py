from django.urls import path

from . import views

app_name = "ticketing"
urlpatterns = [

    path("", views.guacamole_render, name="guacamole"),
    path("submit", views.guacamole_create_user, name="guacamole_create_user"),
]