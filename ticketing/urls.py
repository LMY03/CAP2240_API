from django.urls import path

from . import views

app_name = "ticketing"
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"), #request list
    # path("new-form/", views.RequestFormView.as_view(), name="new-form"),
    # path("new-form-submit/", views.new_form_submit, name="new-form-submit"),
    # path("<int:pk>/details/", views.DetailView.as_view(), name="details"),
    path("", views.guacamole_render, name="home"),
    path("submit", views.guacamole_submit, name="submit"),
]