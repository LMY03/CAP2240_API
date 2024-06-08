from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from proxmox import proxmox
from guacamole import guacamole

# Create your views here.

def renders(request) : 
    return render(request, "vm_provision.html")

def vm_provision_process(node, vm_id, classname, no_of_vm, cpu_cores, ram):

    upids = []
    new_vm_id = []
    for i in range(no_of_vm):
        new_vm_id.append(vm_id + i + 1)
        upids.append(proxmox.clone_vm(node, vm_id, new_vm_id[i])['data'])

    for i in range(no_of_vm):
        proxmox.wait_for_task(node, upids[i])

    # for i in range(no_of_vm):
    #     proxmox.config_vm(node, new_vm_id[i], cpu_cores, ram)

    for i in range(no_of_vm):
        proxmox.start_vm(node, new_vm_id[i])

    for i in range(no_of_vm):
        proxmox.wait_for_vm_start(node, new_vm_id[i]) 

    hostname = []
    for i in range(no_of_vm):
        hostname.append(proxmox.wait_and_get_ip(node, new_vm_id[i]) )

    protocol = "rdp"
    port = {
        'vnc': 5901,
        'rdp': 3389,
        'ssh': 22
    }.get(protocol)
    username = "jin"
    password = "123456"
    parent_identifier = "ROOT"

    guacamole_connection_id = []
    guacamole_username = []
    guacamole_password = []
    for i in range(no_of_vm):
        guacamole_username.append(f"{classname}-{i}")
        guacamole_password.append(User.objects.make_random_password())
        guacamole_connection_id.append(guacamole.create_connection(guacamole_username[i], protocol, port, hostname[i], username, password, parent_identifier))
        guacamole.create_user(guacamole_username[i], guacamole_password[i])
        guacamole.assign_connection(guacamole_username[i], guacamole_connection_id[i])

    return { new_vm_id, guacamole_connection_id, guacamole_username }
    
def vm_provision(request): 

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_id = int(data.get("template_vm_id"))
        classname = data.get("class")
        no_of_vm = int(data.get("no_of_vm"))
        cpu_cores = int(data.get("cpu_cores"))
        ram = int(data.get("ram"))

        data = vm_provision_process(node, vm_id, classname, no_of_vm, cpu_cores, ram)
        
        # return render(request, "vm_deletion.html", { "data" : data })
    
        # for i in range(no_of_vm):
        #     data[i] = vm_provision_process(node, vm_id, vm_id + 1 + i, f"{classname}-{i}")
        

        
        # clone_vm_response = proxmox.clone_vm(node, vmid, new_vm_id)
        # upid = clone_vm_response['data']

        # proxmox.wait_for_task(node, upid)

        # proxmox.start_vm(node, new_vm_id)

        # proxmox.wait_for_vm_start(node, new_vm_id) 

        # hostname = proxmox.wait_for_qemu_start(node, new_vm_id) 

        # guacamole_username = classname
        # guacamole_password = User.objects.make_random_password()
        # guacamole_connection_id = guacamole.create_connection(classname, protocol, port, hostname, username, password, parent_identifier)
        # guacamole.create_user(guacamole_username, guacamole_password)
        # guacamole.assign_connection(guacamole_username, guacamole_connection_id)

        # data = {
        #     'username': guacamole_username,
        #     'password': guacamole_password,
        # }
        return render(request, "data.html", { "data" : data })
    
    return redirect("/ticketing")

def vm_deletion(request):

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_ids = data.getlist("vm_id")
        guacamole_usernames = data.getlist("guacamole_username")
        guacamole_ids = data.getlist("guacamole_id")

        for vm_id in range(vm_ids):
            proxmox.stop_vm(node, vm_id)
            
        for vm_id in range(vm_ids):
            proxmox.delete_vm(node, vm_id)

        for guacamole_username in range(guacamole_usernames):
            guacamole.delete_user(guacamole_username)

        for guacamole_id in range(guacamole_ids):
            guacamole.delete_connection(guacamole_id)

        return render(request, "data.html", { "data" : data })
    
    return redirect("/ticketing")

def render_delete_form(request) : 
    return render(request, "vm_provision.html")