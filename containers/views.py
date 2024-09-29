from django.shortcuts import render, redirect

from . import proxmox

# Create your views here.

def renders(request) : 
    return render(request, "containers/form.html")

def clone_lxc(request):

    if request.method == "POST":

        data = request.POST
        vm_id = data.get("vm_id")
        newid = data.get("newid")

        data = proxmox.clone_lxc("jin", vm_id, newid, newid)

        return render(request, "containers/data.html", { 'data' : data })
    
    return redirect('containers:form')