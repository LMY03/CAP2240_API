from django.http import JsonResponse
from jinja2 import Environment, FileSystemLoader
import ansible_runner
import json
# ansible all -i /ansible/inventory/hosts -m ping -e 'ansible_ssh_common_args="-o StrictHostKeyChecking=no"'

INVENTORY_HOSTS_PATH = '/app/ansible/inventory/hosts'

# def update_inventory_hosts(ip_add, vm_user):
#     inventory_content = """
#     [all]
#     10.10.10.11 ansible_user=jin
#     10.10.10.12 ansible_user=jin
#     """
#     with open(INVENTORY_HOSTS_PATH, 'w') as file:
#         file.write(inventory_content)
#         # file.write(ip_add + ' ansible_user=' + vm_user)
#     # return "File has been edited successfully."

def update_inventory_hosts():
    inventory_content = """
    [all]
    10.10.10.11 ansible_user=jin
    10.10.10.12 ansible_user=jin
    """
    with open(INVENTORY_HOSTS_PATH, 'w') as file:
        file.write(inventory_content)
        # file.write(ip_add + ' ansible_user=' + vm_user)
    # return "File has been edited successfully."

def fetch_hosts(): 
    hosts_data = [
        {"ip": "192.168.254.152", "ansible_user": "jin", "hostname": "Node_2", "label": "S12"},
        {"ip": "192.168.254.153", "ansible_user": "jin", "hostname": "Node_3", "label": "S13"}
    ]
    inventory = {
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "hosts": [],
            "vars": {}
        }
    }

    for host in hosts_data:
        inventory['all']['hosts'].append(host['ip'])
        inventory["_meta"]["hostvars"][host['ip']] = {
            "ansible_user": host['ansible_user'],
            "hostname": host['hostname'],
            "label": host['label']
        }

    return json.dumps(inventory)

def run_playbook(playbook):
    inventory = fetch_hosts()
    print(inventory)
    print('{"test": {"hosts": ["192.168.254.152", "192.168.254.153"], "vars": {}}, "_meta": {"hostvars": {"192.168.254.152": {"ansible_user": "jin", "hostname": "Node_2", "label": "S12"}, "192.168.254.153": {"ansible_user": "jin", "hostname": "Node_3", "label": "S13"}}}}')
    result = ansible_runner.run(
        private_data_dir='/app/ansible',
        playbook=playbook,
        inventory=inventory
    )

    # print("{}: {}".format(r.status, r.rc))
    # # Output the stdout
    # print("stdout: " + r.stdout.read())

    if result.rc == 0:
        return JsonResponse({'status': 'Playbook executed successfully'})
    else:
        return JsonResponse({
            'status': 'Playbook execution failed', 
            'details': result.stdout.read() if result.stdout else 'No output available',
            # 'details': result.stdout.read() if result.stdout else ''
            'message': 'Playbook execution failed'
        })


# def run_playbook():

#     # Define your dynamic host variables
#     hosts = [
#         {
#             "host": "192.168.254.151",
#             "hostname": "Node 1",
#             "label": "S11"
#         },
#         {
#             "host": "192.168.254.152",
#             "hostname": "Node 2",
#             "label": "S12"
#         }
#     ]

#     # Setup Jinja2 environment
#     env = Environment(loader=FileSystemLoader('/app/ansible/project/templates'))
#     template = env.get_template('netdata_config.yml.j2')

#     # Render the playbook content with dynamic values
#     playbook_content = template.render(hosts=hosts)

#     # Define private_data_dir and create directory structure
#     private_data_dir = '/app/ansible'
#     os.makedirs(f"{private_data_dir}/project", exist_ok=True)
#     os.makedirs(f"{private_data_dir}/inventory", exist_ok=True)

#     # Write the rendered playbook to the project directory
#     playbook_path = f'{private_data_dir}/project/playbook.yml'
#     with open(playbook_path, 'w') as playbook_file:
#         playbook_file.write(playbook_content)

#     # Create the inventory file
#     inventory_content = """
#     [all]
#     192.168.254.151
#     192.168.254.152
#     """
#     inventory_path = f'{private_data_dir}/inventory/hosts'
#     with open(inventory_path, 'w') as inventory_file:
#         inventory_file.write(inventory_content)

#     # Run the playbook using ansible-runner
#     result = ansible_runner.run(
#         private_data_dir=private_data_dir,
#         playbook='playbook.yml',
#         inventory='inventory/hosts'
#     )

#     # Check the result
#     if result.rc == 0:
#         return JsonResponse({'status': 'Playbook executed successfully'})
#     else:
#         return JsonResponse({
#             'status': 'Playbook execution failed', 
#             'details': result.stdout.read() if result.stdout else ''
#         })

# def run_command(command): 
#     print(command)
#     try:
#         result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         output = result.stdout.decode() + "\n" + result.stderr.decode()
#     except subprocess.CalledProcessError as e:
#         output = f"Command failed with error code {e.returncode}: {e.output.decode()}"
    
#     return HttpResponse(output, content_type="text/plain")
    
# def run_playbook(playbook):
#     run_command("ansible-playbook -i " + INVENTORY_HOSTS_PATH + " /app/ansible/playbooks/" + playbook + ".yml")
    
# def check_playbook(playbook):
#     run_command("ansible-playbook --check " + playbook + ".yml")

# def run_ansible_lint(playbook):
#     run_command("ansible-lint --check " + playbook + ".yml")

# def test_ping():
#     run_command("ansible all -i " + INVENTORY_HOSTS_PATH + "")