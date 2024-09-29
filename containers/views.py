from django.shortcuts import render

from .proxmox import clone_lxc

# Create your views here.

def renders(request) : 
    return render(request, "form.html")