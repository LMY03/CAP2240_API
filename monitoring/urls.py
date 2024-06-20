from django.urls import path

from . import views

app_name = "monitoring"

urlpatterns = [
    path('', views.vm_monitoring, name='vm_monitoring'),
]