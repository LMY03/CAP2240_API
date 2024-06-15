import subprocess
# import ansible_runner
# ansible all -i /ansible/inventory/hosts -m ping -e 'ansible_ssh_common_args="-o StrictHostKeyChecking=no"'

INVENTORY_HOSTS_PATH = '/ansible/inventory/hosts'
INVENTORY_HOSTS_PATH = '/ansible/inventory/hosts'

def test_ping():
    run_command("ansible all -i " + INVENTORY_HOSTS_PATH + "")

def update_inventory_hosts(ip_add, vm_user):
    print("update inventory")
    with open(INVENTORY_HOSTS_PATH, 'w') as file:
        file.write(ip_add + ' ansible_user=' + vm_user)
    return "File has been edited successfully."

def run_command(command): 
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return str(e)
    
def run_playbook(playbook):
    run_command("ansible-playbook -i " + INVENTORY_HOSTS_PATH + " /app/playbooks/" + playbook + " .yml")
    
def check_playbook(playbook):
    run_command("ansible-playbook --check " + playbook + ".yml")

def run_ansible_lint(playbook):
    run_command("ansible-lint --check " + playbook + ".yml")