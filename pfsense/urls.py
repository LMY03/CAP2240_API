from django.urls import path

from . import views

app_name = "pfsense"

urlpatterns = [
    path('', views.renders, name='index'),
    path('add_firewall_rule', views.add_firewall_rule, name='add_firewall_rule'),
    path('edit_firewall_rule', views.edit_firewall_rule, name='edit_firewall_rule'),
    path('delete_firewall_rule', views.delete_firewall_rule, name='delete_firewall_rule'),
    path('get_rules', views.get_rules, name='get_rules'),
]