from django.shortcuts import render

import ansible_runner, os
from django.http import JsonResponse

# Create your views here.

def renders(request) : 
    return render(request, "ansible.html")

def run(request):
    if request.method == "POST":
        return render(request, "data.html", { "data" : run_playbook() })

def run_playbook():
    playbook_path = '/playbooks/playbook.yml'  # Updated path
    inventory_path = '/inventory/hosts'
    private_data_dir = '/tmp/'

    r = ansible_runner.run(private_data_dir=private_data_dir, playbook=playbook_path, inventory=inventory_path)

    if r.status == 'successful':
        return JsonResponse({'status': 'success', 'data': r.get_fact_cache()})
    else:
        stderr_path = os.path.join(private_data_dir, 'artifacts', r.rc, 'stderr')
        try:
            with open(stderr_path, 'r') as stderr_file:
                stderr_output = stderr_file.read()
        except Exception as e:
            stderr_output = f"Error reading stderr file: {e}"
        return JsonResponse({'status': 'failure', 'data': stderr_output})