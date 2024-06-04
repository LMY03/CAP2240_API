from django.urls import path

from . import views

app_name = "ticketing"
urlpatterns = [
    path("new-form/", views.RequestFormView.as_view(), name="new-form"),
    path("new-form-submit/", views.new_form_submit, name="new-form-submit"),
]