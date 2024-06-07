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
            return task_status['data']['exitstatus']
        time.sleep(5)

def wait_for_vm_start(node, vmid):
    while True:
        status_response = proxmox.get_vm_status(node, vmid)
        status = status_response
        if status == 'running':
            break
        time.sleep(5)

def clone_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")
        newid = data.get("newid")

        clone_vm_response = proxmox.clone_vm(node, vmid, newid)
        upid = clone_vm_response['data']

        clone_status  = wait_for_task(node, upid)

        return render(request, "data.html", { "data" : clone_status })
        
    return redirect("/proxmox")

def start_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        proxmox.start_vm(node, vmid)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")

def shutdown_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        proxmox.shutdown_vm(node, vmid)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")

def delete_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        proxmox.delete_vm(node, vmid)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")

def stop_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        proxmox.stop_vm(node, vmid)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")

def status_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        status = proxmox.get_vm_status(node, vmid)

        return render(request, "status_vm.html", { "status" : status })
        
    return redirect("/proxmox")

def ip_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        ip = proxmox.get_vm_ip(node, vmid)

        context = { "ip" : ip }

        return render(request, "ip_add.html", context)
        
    return redirect("/proxmox")

def config_vm(request) : 

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")
        cpu = data.get("cpu")
        memory = data.get("memory")

        proxmox.config_vm(node, vmid, cpu, memory)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")