from django.shortcuts import render, redirect

import redis

from . import pfsense

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Create your views here.

def get_port_forward_rule(vm_name):
    rules = pfsense.get_port_forward_rules()
    for rule in rules:
        if rule['descr'] == vm_name: return rule


def get_port_forward_rules(request_id):
    rules = pfsense.get_port_forward_rules()
    for rule in rules:
        if rule['descr'] == "Test": return rule['id']


def create_firewall_rule():
    lock = redis_client.lock('pfsense_lock', timeout=10)
    with lock:
        pfsense.add_firewall_rule()
        pfsense.apply_changes()

def update_firewall_rule_ip_add(vm_name):
    lock = redis_client.lock('pfsense_lock', timeout=10)
    with lock:
        get_firewall_rule(vm_name)

def delete_firewall_rule(vm_name):
    lock = redis_client.lock('pfsense_lock', timeout=10)
    with lock:
        get_firewall_rule(vm_name)

def renders(request):
    return render(request, 'pfsense.html')

def add_firewall_rule(request):

    if request.method == 'POST':

        data = request.POST
        protocol = data.get("protocol")
        destination_port = data.get("destination_port")
        ip_add = data.get("ip_add")
        local_port = data.get("local_port")

        response = pfsense.add_firewall_rule(protocol, destination_port, ip_add, local_port)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def edit_firewall_rule(request):

        
    if request.method == 'POST':

        data = request.POST
        id = data.get("id")
        ip_add = data.get("ip_add")

        response = pfsense.edit_firewall_rule(id, ip_add)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def delete_firewall_rule(request):

    if request.method == 'POST':

        data = request.POST
        id = data.get("id")

        response = pfsense.delete_firewall_rule(id)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def get_port_forward_rules(request):
    data = get_port_forward_rule("Test")
    return render(request, 'data.html', { 'data' : data })

def get_firewall_rules(request):
    data = pfsense.get_firewall_rules()
    return render(request, 'data.html', { 'data' : data })