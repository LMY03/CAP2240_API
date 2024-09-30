from decouple import config
import requests, time

from proxmoxer import ProxmoxAPI

PROXMOX_HOST = config('PROXMOX_HOST')
PROXMOX_IP = config('PROXMOX_IP')
PROXMOX_PORT = config('PROXMOX_PORT')
PROXMOX_USERNAME = config('PROXMOX_USERNAME')
PROXMOX_PASSWORD = config('PROXMOX_PASSWORD')
# CA_CRT = config('CA_CRT')
CA_CRT = False
STORAGE = 'local-lvm'

# proxmox = ProxmoxAPI('10.1.200.11', user='root@pam', password='cap2240', verify_ssl=CA_CRT)
# proxmox = ProxmoxAPI(PROXMOX_IP, user=PROXMOX_USERNAME, password=PROXMOX_PASSWORD, verify_ssl=CA_CRT)

def get_proxmox_client():
    proxmox = ProxmoxAPI(
        host=PROXMOX_IP,
        user=PROXMOX_USERNAME,
        password=PROXMOX_PASSWORD,
        verify_ssl=CA_CRT
    )
    return proxmox

# clone_lxc

# create_snapshot
def create_snapshot(node, vm_id, snapshot_name="automation_snapshot"):
    get_proxmox_client().nodes(node).lxc(vm_id).snapshot().create(snapname=snapshot_name)
    return snapshot_name

def delete_snapshot(node, vm_id, snapshot_name):
    get_proxmox_client().nodes(node).lxc(vm_id).snapshot(snapshot_name).delete()

# full clone snapshot
def clone_container(node, vm_id, snapshot, new_vm_id, new_vm_name):
    get_proxmox_client().nodes(node).lxc(vm_id).clone().create(
        newid=new_vm_id,
        hostname=new_vm_name,
        full=1,
        snapname=snapshot
    )

def check_clone_status(node, vm_id):
    task_status = get_proxmox_client().nodes(node).tasks().get()
    for task in task_status:
        if task['upid'].startswith(f"UPID:{node}:{vm_id}:") and task['status'] == 'running':
            return False
    return True

def start_lxc(node, vm_id):
    get_proxmox_client().nodes(node).lxc(vm_id).status().start()


def get_ip_address(node, vm_id):
    network_info = get_proxmox_client().nodes(node).lxc(vm_id).config().get()
    ip_address = network_info.get('ens18', {}).get('ip', None)
    return ip_address

def clone_lxc(node, vm_id, new_vm_ids, new_names):
    # Initialize Proxmox API connection
    proxmox = ProxmoxAPI('10.1.200.11', user='root@pam', password='cap2240', verify_ssl=False)

    for new_id, new_name in zip(new_vm_ids, new_names):
        try:
            print(f"Starting clone operation for new container ID: {new_id} with name: {new_name}")
            
            # Perform the clone operation
            task = proxmox.nodes(node).lxc(vm_id).clone.post(
                newid=new_id,
                target=node,
                full=1,
                storage='local-lvm',
            )
            print(f"Successfully cloned LXC ID '{vm_id}' to new ID '{new_id}'.")

            # Use config.put to clear the lock instead of status.unlock.post
            print(f"Clearing the lock for the cloned container {new_id}...")
            proxmox.nodes(node).lxc(new_id).config.put(
                lock=None
            )
            print(f"Container {new_id} lock cleared successfully.")

            # Optional: Start the container if needed
            print(f"Starting container {new_id}...")
            proxmox.nodes(node).lxc(new_id).status.start.post()
            print(f"Container {new_id} started successfully.")

        except Exception as e:
            print(f"Clone operation failed for ID {new_id}. Error: {e}")

    # for new_id in new_vm_ids:
    #     print(f"Starting container {new_id}...")
    #     proxmox.nodes(node).lxc(new_id).status.start.post()
    #     print(f"Container {new_id} started successfully.")

    # Step 4: Retrieve the IP addresses of the new containers
    # ip_addresses = []
    # for new_id in new_vm_ids:
    #     # Wait a few seconds to allow the container to fully boot and retrieve its IP
    #     time.sleep(5)
    #     status = proxmox.nodes(node).lxc(new_id).status.current.get()
    #     # Extract the IP address
    #     ip_address = None
    #     if "data" in status and "ens18" in status['data']:
    #         ip_info = status['data']['net0'].get('ip-addresses', [])
    #         # Filter for a valid IPv4 address (not a link-local address)
    #         ip_address = next((ip['ip'] for ip in ip_info if ip['family'] == 'inet'), None)

    #     ip_addresses.append(ip_address)
    #     print(f"Container {new_id} has IP address: {ip_address}")

    # return ip_addresses
