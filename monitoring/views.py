from django.shortcuts import render

# Create your views here.

def renders(request) : 
    ip_add = {
        "192.168.254.165",
        "192.168.254.166",
    }
    return render(request, "monitoring.html", { "ip_add" : ip_add })