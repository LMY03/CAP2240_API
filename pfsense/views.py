from django.shortcuts import render, redirect

from . import pfsense

# Create your views here.

def renders(request):
    return render(request, 'pfsense.html')

def add_firewall_rule(request):

    if request.method == 'POST':

        data = request.POST
        destination = data.get("destination")
        protocol = data.get("protocol")
        destination_port = data.get("destination_port")
        ip_add = data.get("ip_add")
        local_port = data.get("local_port")

        response = pfsense.add_firewall_rule(protocol, destination_port, ip_add, local_port)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def edit_firewall_rule(request):

        
    if request.method == 'POST':

        data = request.POST
        id = data.get("id")
        ip_add = data.get("ip_add")

        response = pfsense.edit_firewall_rule(id, ip_add)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def delete_firewall_rule(request):

    if request.method == 'POST':

        data = request.POST
        id = data.get("id")

        response = pfsense.delete_firewall_rule(id)

        return render(request, 'data.html', { 'data' : response })

    return redirect('/pfsense')

def get_rules(request):
    print("------------------------")
    data = pfsense.get_rules()
    return render(request, 'data.html', { 'data' : data })