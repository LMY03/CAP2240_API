from django.shortcuts import render

from . import ansible
from django.http import JsonResponse

# Create your views here.

def renders(request) : 
    return render(request, "ansible.html")

def run(request):
    if request.method == "POST":

        data = request.POST
        command = data.get("command")

        ip_add = "10.164.113.224"
        vm_user = "jin"
        ansible.update_inventory_hosts(ip_add, vm_user)

        return render(request, "data.html", { "data" : ansible.run_command(command) })

# def run_ansible_playbook():
#     try:
#         # command = "docker exec ansible_service ansible-playbook /playbooks/playbook.yml"
#         command = "docker exec -it ansible ansible all -i /inventory/hosts -m ping"
#         result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
#         return result.stdout.decode()
#     except subprocess.CalledProcessError as e:
#         return str(e)
    
# def run_ansible_playbook(playbook):
#     return run_command("ansible-playbook " + "/playbooks/" + playbook + ".yml")



# def run_playbook():
#     playbook_path = '/playbooks/playbook.yml'
#     inventory_path = '/inventory/hosts'

#     r = ansible_runner.run(private_data_dir='/tmp/', playbook=playbook_path, inventory=inventory_path)

#     if r.status == 'successful':
#         return JsonResponse({'status': 'success', 'data': r.get_fact_cache()})
#     else:
#         return JsonResponse({'status': 'failure', 'data': r.stderr})