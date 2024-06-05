from django.shortcuts import redirect, render

from . import proxmox

# Create your views here.

node = "pve"

def renders(request) : 
    return render(request, "proxmox.html")

def success(request) : 
    return render(request, "success.html")

def clone_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")
        newid = data.get("newid")

        proxmox.clone_vm(node, vmid, newid)

        return redirect("/proxmox/success")
        
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

        context = { "status" : status }

        return render(request, "status_vm.html", context)
        
    return redirect("/proxmox")

def ip_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        ip = proxmox.get_vm_ip(node, vmid)

        context = { "ip" : ip }

        return render(request, "ip_vm.html", context)
        
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