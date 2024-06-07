from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from proxmox import proxmox
from guacamole import guacamole

# Create your views here.

def renders(request) : 
    return render(request, "vm_provision.html")

def vm_provision(request) : 

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

        new_vm_id = proxmox.clone_vm("pve", vmid, 999)

        hostname = proxmox.get_vm_ip(node, new_vm_id)
        guacamole_password = User.objects.make_random_password()
        guacamole_connection_id = guacamole.create_connection(classname, protocol, port, hostname, username, password, parent_identifier)
        guacamole_username = guacamole.create_user(classname, guacamole_password)
        guacamole.assign_connection(guacamole_username, guacamole_connection_id)



        return render(request, "data.html", { "data" : None })
    
    return redirect("/ticketing")