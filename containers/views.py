from django.shortcuts import render, redirect

from . import proxmox

# Create your views here.

def renders(request) : 
    return render(request, "containers/form.html")

def clone_lxc(request):
    if request.method == "POST":

        data = request.POST
        vmid = [data.get("vmid")]
        newid = [data.get("newid")]

        newid = ['4002', '4003']

        data = proxmox.clone_lxc("pve", vmid, newid, newid)

        return render(request, "containers/data.html", { 'data' : data })
    
    # return redirect('containers:form')