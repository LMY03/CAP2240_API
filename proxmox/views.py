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

        proxmox.delete_vm(node, vmid)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")

def delete_vm(request) :

    if request.method == "POST":

        data = request.POST
        vmid = data.get("vmid")

        proxmox.delete_vm(node, vmid)

        return redirect("/proxmox/success")
        
    return redirect("/proxmox")