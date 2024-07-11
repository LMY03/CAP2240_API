from django.urls import path

from . import views

app_name = "pfsense"

urlpatterns = [
    path('', views.renders, name='index'),
    path('test_run', views.test_run, name='test_run'),
    # path('add_port_forward_rule', views.add_port_forward_rule, name='add_port_forward_rule'),
    # path('edit_port_forward_rule', views.edit_port_forward_rule, name='edit_port_forward_rule'),
    # path('delete_port_forward_rule', views.delete_port_forward_rule, name='delete_port_forward_rule'),
    # path('get_port_forward_rules', views.get_port_forward_rules, name='get_port_forward_rules'),
    # path('get_firewall_rules', views.get_firewall_rules, name='get_firewall_rules'),
]