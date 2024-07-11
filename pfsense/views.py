from django.shortcuts import render, redirect
import time
from . import pfsense

# Create your views here.

def renders(request): return render(request, 'test.html')

def add_rules(request):
    add_port_forward_rules(1)
    return redirect('/pfsense')

def delete_rules(request):
    delete_port_forward_rules(['VM1', 'VM2', 'VM3'])
    return redirect('/pfsense')

def get_port_forward_rule(vm_name):
    rules = pfsense.get_port_forward_rules()
    for rule in rules:
        if rule['descr'] == vm_name: return rule['id']

def get_firewall_rule(vm_name):
    rules = pfsense.get_firewall_rules()
    for rule in rules:
        if rule['descr'] == vm_name : return rule['id']

# def generate_dest_ports():
#     port_rules = []
#     request_entries = RequestEntry.objects.filter(status=RequestEntry.Status.ONGOING) # maybe also add completed
#     for request_entry in request_entries:
#         for port_rule in PortRules.objects.filter(request_id=request_entry.id):
#             port_rules.append(port_rule)

#     return

def add_port_forward_rules(request_id):
    # vms = VirtualMachines.objects.filter(request_id=request_id)
    # port_rules = PortRules.objects.filter(request_id=request_id)
    
    # protocols = port_rules.values_list('protocol', flat=True)
    # dest_ports = port_rules.values_list('dest_ports', flat=True)
    # ip_adds = vms.values_list('ip_add', flat=True)
    # descrs = vms.values_list('vm_name', flat=True)

    protocol = 'tcp'
    local_port = '80'
    dest_ports = ['1000', '1001', '1002']
    ip_adds = ['192.168.2.1', '192.168.2.2', '192.168.2.3']
    descrs = ['VM1', 'VM2', 'VM3']

    # dest_ports = generate_dest_ports()
    for destination_port, ip_add, descr in zip(dest_ports, ip_adds, descrs):
        pfsense.add_firewall_rule(protocol, destination_port, ip_add, descr)
        pfsense.add_port_forward_rule(protocol, destination_port, ip_add, local_port, descr)
    pfsense.apply_changes()

# def update_port_forward_rule_ip_adds(vm_names, ip_adds):
#     for vm_name, ip_add in vm_names, ip_adds:
#         port_forward_id = get_port_forward_rule(vm_name)
#         firewall_id = get_firewall_rule(vm_name)
#         pfsense.edit_port_forward_rule(port_forward_id, ip_add)
#         pfsense.edit_firewall_rule(firewall_id, ip_add)

def delete_port_forward_rules(vm_names):
    for vm_name in vm_names:
        # get_firewall_rule(vm_name)
        pfsense.delete_firewall_rule(get_firewall_rule(vm_name))
        pfsense.delete_port_forward_rule(get_port_forward_rule(vm_name))
        time.sleep(3)