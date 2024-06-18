from django.shortcuts import redirect, render
from django.http import JsonResponse

from django.contrib.auth.models import User

from proxmox import proxmox
from guacamole import guacamole
from autotool import ansible

# Create your views here.

def renders(request) : 
    return render(request, "form.html")

def vm_provision_process(node, vm_id, classname, no_of_vm, cpu_cores, ram):

    protocol = "rdp"
    port = {
        'vnc': 5901,
        'rdp': 3389,
        'ssh': 22
    }.get(protocol)
    username = "jin"
    password = "123456"
    parent_identifier = "ROOT"

    upids = []
    new_vm_id = []
    hostname = []
    guacamole_connection_id = []
    guacamole_username = []
    guacamole_password = []

    for i in range(no_of_vm):
        # clone vm
        new_vm_id.append(vm_id + i + 1)
        upids.append(proxmox.clone_vm(node, vm_id, new_vm_id[i])['data'])

    for i in range(no_of_vm):
        # wait for vm to clone
        proxmox.wait_for_task(node, upids[i])
        # change vm configuration
        proxmox.config_vm(node, new_vm_id[i], cpu_cores, ram)
        # start vm
        proxmox.start_vm(node, new_vm_id[i])

    
    for i in range(no_of_vm):
        # wait for vm to start
        proxmox.wait_for_vm_start(node, new_vm_id[i])
        hostname.append(proxmox.wait_and_get_ip(node, new_vm_id[i]) )
        # create connection
        guacamole_username.append(f"{classname}-{i}")
        # guacamole_password.append(User.objects.make_random_password())
        guacamole_password.append("123456")
        guacamole_connection_id.append(guacamole.create_connection(guacamole_username[i], protocol, port, hostname[i], username, password, parent_identifier))
        guacamole.create_user(guacamole_username[i], guacamole_password[i])
        guacamole.assign_connection(guacamole_username[i], guacamole_connection_id[i])

        # set hostname and label in netdata
    vm_user = []
    vm_name = []
    label = []

    for i in range(no_of_vm):
        vm_user.append("jin")
        vm_name.append(classname + "-" + str(i))
        label.append(classname)

    ansible.run_playbook("netdata_conf.yml", hostname, vm_user, vm_name, label)

    return { 
        'vm_id' : new_vm_id, 
        'guacamole_connection_id' : guacamole_connection_id, 
        'guacamole_username' : guacamole_username
    }
    
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
        
        return render(request, "vm_deletion.html", { "data" : data })
    
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
        # return render(request, "data.html", { "data" : data })
    
    return redirect("/ticketing")

def vm_deletion(request):

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_ids = data.getlist("vm_id")
        guacamole_usernames = data.getlist("guacamole_username")
        guacamole_ids = data.getlist("guacamole_connection_id")

        for vm_id in vm_ids:
            proxmox.stop_vm(node, vm_id)
            
        for vm_id in vm_ids:
            proxmox.wait_for_vm_stop(node, vm_id)
            proxmox.delete_vm(node, vm_id)

        for guacamole_username in guacamole_usernames:
            guacamole.delete_user(guacamole_username)

        for guacamole_id in guacamole_ids:
            guacamole.delete_connection(guacamole_id)
    
    return redirect("/ticketing")

# Start VM -> Check IP -> Update Connection (if needed) -> Open Connection
def launch_vm(request):

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_id = data.get("vm_id")
        connection_id = data.get("connection_id")
        guacamole_username = data.get("username")
        # guacamole_password = data.get("guacamole_password")
        guacamole_password = "123456"

        if proxmox.get_vm_status(node, vm_id) == "stopped" : proxmox.start_vm(node, vm_id)
        hostname = proxmox.wait_and_get_ip(node, vm_id)
        connection_details = guacamole.get_connection_parameter_details(connection_id)
        if hostname != connection_details['hostname'] : guacamole.update_connection(connection_id, hostname)
        
        # redirect to new tab
        url =  guacamole.get_connection_url(connection_id, guacamole_username, guacamole_password)
        
        return JsonResponse({"redirect_url": url})
    
    return redirect("/ticketing")

def lxc_provision(request): 

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_id = int(data.get("template_vm_id"))
        classname = data.get("class")
        no_of_vm = int(data.get("no_of_vm"))
        cpu_cores = int(data.get("cpu_cores"))
        ram = int(data.get("ram"))

        data = lxc_provision_process(node, vm_id, classname, no_of_vm, cpu_cores, ram)
        
        return render(request, "lxc_deletion.html", { "data" : data })

def lxc_provision_process(node, vm_id, classname, no_of_vm, cpu_cores, ram):
    new_vm_id = []
    hostname = []

    # maybe use ansible to clone containers
    for i in range(no_of_vm):
        new_vm_id.append(vm_id + i + 1)
        proxmox.clone_lxc(node, vm_id, new_vm_id[i])
        proxmox.wait_for_lxc_lock(node, vm_id)
        proxmox.config_lxc(node, new_vm_id[i], cpu_cores, ram)
        proxmox.start_lxc(node, new_vm_id[i])
    
    for i in range(no_of_vm):
        # wait for vm to start
        proxmox.wait_for_lxc_start(node, new_vm_id[i])
        hostname.append(proxmox.wait_and_get_lxc_ip(node, new_vm_id[i]))

    vm_user = []
    vm_name = []
    label = []

    for i in range(no_of_vm):
        vm_user.append("jin")
        vm_name.append(classname + "-" + str(i))
        label.append(classname)

    ansible.run_playbook("netdata_conf.yml", hostname, vm_user, vm_name, label)

    return { 
        'vm_id' : new_vm_id,
        'hostname' : hostname
    }

def launch_lxc(request):

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_id = data.get("vm_id")
        
        response = proxmox.start_lxc(node, vm_id)
        
        return JsonResponse({"redirect_url": response})
    
    return redirect("/ticketing")

def lxc_deletion(request):

    if request.method == "POST":

        node = "pve"

        data = request.POST
        vm_ids = data.getlist("vm_id")

        for vm_id in vm_ids:
            proxmox.stop_lxc(node, vm_id)
            
        for vm_id in vm_ids:
            proxmox.wait_for_lxc_stop(node, vm_id)
            proxmox.delete_lxc(node, vm_id)

    return redirect("/ticketing")