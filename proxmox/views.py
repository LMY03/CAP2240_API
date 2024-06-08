import time

from django.shortcuts import redirect, render

from . import proxmox

# Create your views here.

node = "pve"

def renders(request) : 
    return render(request, "proxmox.html")

def wait_for_task(node, upid): 
    while True:
        task_status = proxmox.get_task_status(node, upid)
        if task_status['data']['status'] == 'stopped':
            return task_status['data']['exitstatus'] # OK
        time.sleep(5)

def wait_for_vm_start(node, vmid):
    while True:
        status = proxmox.get_vm_status(node, vmid)
        if status == "running" : return status
        time.sleep(5)

def wait_for_qemu_start(node, vmid):
    while True:
        # qemu_status_code = proxmox.get_qemu_status(node, vmid)
        # if qemu_status_code == 200:
        response = proxmox.get_vm_ip(node, vmid)
        if response['data'] != 'None' :
            for interface in response['data']['result']:
                if interface['name'] == "ens18":
                    print("interface")
                    # print(interface)
                    # print("-------------------------")
                    if 'ip-addresses' not in interface: continue  
                    for ip in interface['ip-addresses']:
                        if ip['ip-address-type'] == 'ipv4':
                            # print("ip")
                            # print(ip)
                            # print("ipv4")
                            # print(ip['ip-address'])
                            # print("-------------------------")
                            return ip['ip-address']
        time.sleep(5)

# def get_vm_ip():
#     while True:
#         if status == 
#         time.sleep(5)

def clone_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")
        new_vm_id = data.get("newid")

        clone_vm_response = proxmox.clone_vm(node, vmid, new_vm_id)
        upid = clone_vm_response['data']

        wait_for_task(node, upid)

        proxmox.start_vm(node, new_vm_id)

        wait_for_vm_start(node, new_vm_id) 

        response = wait_for_qemu_start(node, new_vm_id) 
        # response = proxmox.get_vm_ip(node, new_vm_id)

        

        return render(request, "data.html", { "data" : response })
        
    return redirect("/proxmox")

def start_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        response = proxmox.start_vm(node, vmid)

        return render(request, "data.html", { "data" : response })
        
    return redirect("/proxmox")

def shutdown_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        response = proxmox.shutdown_vm(node, vmid)

        return render(request, "data.html", { "data" : response })
        
    return redirect("/proxmox")

def delete_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        response = proxmox.delete_vm(node, vmid)

        return render(request, "data.html", { "data" : response })
        
    return redirect("/proxmox")

def stop_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        response = proxmox.stop_vm(node, vmid)

        return render(request, "data.html", { "data" : response })
        
    return redirect("/proxmox")

def status_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        status = proxmox.get_vm_status(node, vmid)

        return render(request, "data.html", { "data" : status })
        
    return redirect("/proxmox")

def ip_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        ip = proxmox.get_vm_ip(node, vmid)

        return render(request, "data.html", { "data" : ip })
        
    return redirect("/proxmox")

def config_vm(request) : 

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")
        cpu_cores = data.get("cpu")
        memory = data.get("memory")

        response = proxmox.config_vm(node, vmid, cpu_cores, memory)

        return render(request, "data.html", { "data" : response })
    
    return redirect("/proxmox")