from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from proxmox import proxmox
from guacamole import guacamole

# Create your views here.

def renders(request) : 
    return render(request, "vm_provision.html")

def vm_provision_process(node, vm_id, classname, no_of_vm):

    upids = []
    new_vm_id = []
    for i in range(no_of_vm):
        new_vm_id.append(vm_id + i + 1)
        upids.append(proxmox.clone_vm(node, vm_id, new_vm_id[i])['data'])

    for i in range(no_of_vm):
        proxmox.wait_for_task(node, upids[i])

    for i in range(no_of_vm):
        proxmox.start_vm(node, new_vm_id[i])

    for i in range(no_of_vm):
        proxmox.wait_for_vm_start(node, new_vm_id[i]) 

    hostname = []
    for i in range(no_of_vm):
        hostname.append(proxmox.wait_for_qemu_start(node, new_vm_id[i]) )

    protocol = "rdp"
    port = {
        'vnc': 5901,
        'rdp': 3389,
        'ssh': 22
    }.get(protocol)
    username = "jin"
    password = "123456"
    parent_identifier = "ROOT"

    guacamole_username = []
    guacamole_password = []
    for i in range(no_of_vm):
        guacamole_username.append(f"{classname}-{i}")
        guacamole_password.append(User.objects.make_random_password())
        guacamole_connection_id = guacamole.create_connection(guacamole_username[i], protocol, port, hostname[i], username, password, parent_identifier)
        guacamole.create_user(guacamole_username[i], guacamole_password[i])
        guacamole.assign_connection(guacamole_username[i], guacamole_connection_id)
    
def vm_provision(request): 

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_id = int(data.get("vm"))
        classname = data.get("class")
        no_of_vm = int(data.get("no"))

        data = vm_provision_process(node, vm_id, classname, no_of_vm)
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

def vm_test(request):
    if request.method == "POST":
        node = "pve"
        new_vm_id = 999
        proxmox.start_vm(node, new_vm_id)

        proxmox.wait_for_vm_start(node, new_vm_id) 

        hostname = proxmox.wait_for_qemu_start(node, new_vm_id) 

        # print("hostname")
        # print(hostname)
        # print("-------------------------")

        # guacamole_password = User.objects.make_random_password()
        # print("guacamole_password")
        # print(guacamole_password)
        # print("-------------------------")
        # guacamole_connection_id = guacamole.create_connection("Test", 'rdp', '3389', hostname, "jin", "123456", "ROOT")
        # print("guacamole_connection_id")
        # print(guacamole_connection_id)
        # print("-------------------------")
        # guacamole_username = guacamole.create_user("Test", guacamole_password)
        # print("guacamole_username")
        # print(guacamole_username)
        # print("-------------------------")
        # status = guacamole.assign_connection("Test", guacamole_connection_id)
        # print("status")
        # print(status)
        # print("-------------------------")

        # data = {
        #     'hostname': hostname,
        #     'username': guacamole_username,
        #     'password': guacamole_password,
        # }

        return render(request, "data.html", { "data" : hostname })