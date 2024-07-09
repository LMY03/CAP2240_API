from django.shortcuts import render, redirect

from . import pfsense

# Create your views here.

def renders(request):
    return render(request, 'pfsense.html')

def add_rule(request):

    if request.method == 'POST':
        data = pfsense.edit_firewall_rule(4)
        # data = opnsense.get_firewall_rule("c423352c-d132-438f-be10-d86f6a429244")

        return render(request, 'data.html', { 'data' : data })

    return redirect('/pfsense')

def get_rules(request):
    print("------------------------")
    data = pfsense.get_rules()
    print("data")
    print(data)
    return render(request, 'data.html', { 'data' : data })