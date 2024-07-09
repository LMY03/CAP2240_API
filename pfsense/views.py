from django.shortcuts import render, redirect

import redis

from . import pfsense

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# Create your views here.

def get_port_forward_rule(vm_name):
    rules = pfsense.get_port_forward_rules()
    for rule in rules:
        if rule['descr'] == vm_name: return rule['id']
def get_port_forward_rule(vm_name):
    rules = pfsense.get_port_forward_rules()
    for rule in rules:
        if rule['descr'] == vm_name: return rule['id']

# def get_port_forward_rules(vm_names):
#     rules = pfsense.get_port_forward_rules()
#     rule_ids = []
#     for rule in rules:
#         for vm_name in vm_names:
#             if rule['descr'] == vm_name : rule_ids.append({'id': rule['id'], 'name': rule['descr']})
#     return rule_ids

def add_port_forward_rules(protocols, destination_ports, ip_adds, local_ports, descrs):
    lock = redis_client.lock('pfsense_lock', timeout=60)
    with lock:
        for protocol, destination_port, ip_add, local_port, descr in protocols, destination_ports, ip_adds, local_ports, descrs:
            pfsense.add_port_forward_rule(protocol, destination_port, ip_add, local_port, descr)
    pfsense.apply_changes()

def update_port_forward_rule_ip_adds(vm_names, ip_adds):
    lock = redis_client.lock('pfsense_lock', timeout=60)
    with lock:
        for vm_name, ip_add in vm_names, ip_adds:
            id = get_port_forward_rule(vm_name)
            pfsense.edit_port_forward_rule(id, ip_add)

def delete_port_forward_rules(vm_names):
    lock = redis_client.lock('pfsense_lock', timeout=60)
    with lock:
        for vm_name in vm_names:
            id = get_port_forward_rule(vm_name)
            pfsense.delete_port_forward_rule(id)

###########################################################################

def renders(request):
    return render(request, 'pfsense.html')

def add_port_forward_rule(request):

    if request.method == 'POST':

        data = request.POST
        protocol = data.get("protocol")
        destination_port = data.get("destination_port")
        ip_add = data.get("ip_add")
        local_port = data.get("local_port")
        descr = data.get("descr")

        response = add_port_forward_rules(protocol, destination_port, ip_add, local_port, descr)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def edit_port_forward_rule(request):

    if request.method == 'POST':

        data = request.POST
        id = data.get("id")
        ip_add = data.get("ip_add")

        response = pfsense.edit_port_forward_rule(id, ip_add)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def delete_port_forward_rule(request):

    if request.method == 'POST':

        data = request.POST
        id = data.get("id")

        response = pfsense.delete_port_forward_rule(id)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def get_port_forward_rules(request):
    data = get_port_forward_rule("Test")
    return render(request, 'data.html', { 'data' : data })

def get_firewall_rules(request):
    data = pfsense.get_firewall_rules()
    return render(request, 'data.html', { 'data' : data })