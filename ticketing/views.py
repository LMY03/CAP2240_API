from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from proxmox import proxmox, views
from guacamole import guacamole

# Create your views here.

def renders(request) : 
    return render(request, "vm_provision.html")

def vm_test(request):
    if request.method == "POST":
        node = "pve"
        new_vm_id = 999
        proxmox.start_vm(node, new_vm_id)

        views.wait_for_vm_start(node, new_vm_id) 

        hostname = views.wait_for_qemu_start(node, new_vm_id) 

        # guacamole_password = User.objects.make_random_password()
        # guacamole_connection_id = guacamole.create_connection(classname, protocol, port, hostname, username, password, parent_identifier)
        # guacamole_username = guacamole.create_user(classname, guacamole_password)
        # guacamole.assign_connection(guacamole_username, guacamole_connection_id)

        # data = {
        #     'username': guacamole_username,
        #     'password': guacamole_password,
        # }

        return render(request, "data.html", { "data" : hostname })

def vm_provision(request): 

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vmid = data.get("vm")
        classname = data.get("class")

        protocol = "rdp"
        username = "jin"
        password = "123456"
        parent_identifier = "ROOT"

        port = {
            'vnc': 5901,
            'rdp': 3389,
            'ssh': 22
        }.get(protocol)

        new_vm_id = 999

        # new_vm_id = proxmox.clone_vm("pve", vmid, 999)

        # hostname = proxmox.get_vm_ip(node, new_vm_id)
        clone_vm_response = proxmox.clone_vm(node, vmid, new_vm_id)
        upid = clone_vm_response['data']

        views.wait_for_task(node, upid)

        proxmox.start_vm(node, new_vm_id)

        views.wait_for_vm_start(node, new_vm_id) 

        hostname = views.wait_for_qemu_start(node, new_vm_id) 

        guacamole_password = User.objects.make_random_password()
        guacamole_connection_id = guacamole.create_connection(classname, protocol, port, hostname, username, password, parent_identifier)
        guacamole_username = guacamole.create_user(classname, guacamole_password)
        guacamole.assign_connection(guacamole_username, guacamole_connection_id)

        data = {
            'username': guacamole_username,
            'password': guacamole_password,
        }

        return render(request, "data.html", { "data" : data })
    
    return redirect("/ticketing")