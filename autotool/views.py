from django.shortcuts import render

import ansible_runner
from django.http import JsonResponse

# Create your views here.

def renders(request) : 
    return render(request, "ansible.html")

def run(request):
    if request.method == "POST":
        return render(request, "data.html", { "data" : run_playbook() })

def run_playbook():
    playbook_path = '/playbooks/playbook.yml'
    inventory_path = '/inventory/hosts'

    r = ansible_runner.run(private_data_dir='/tmp/', playbook=playbook_path, inventory=inventory_path)

    if r.status == 'successful':
        return JsonResponse({'status': 'success', 'data': r.get_fact_cache()})
    else:
        return JsonResponse({'status': 'failure', 'data': r.stderr})