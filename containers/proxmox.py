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

def clone_lxc(node, vm_id, new_vm_ids, new_names):
    # Initialize Proxmox API connection
    proxmox = ProxmoxAPI('10.1.200.11', user='root@pam', password='cap2240', verify_ssl=CA_CRT)

    # Proceed with the clone operation
    for new_id, new_name in zip(new_vm_ids, new_names):
        try:
            proxmox.nodes(node).lxc(vm_id).clone.post(
                newid=new_id,
                name=new_name,
                target=node,
                full=1,
                storage=STORAGE,
            )
            print(f"Successfully cloned LXC ID '{vm_id}' to new ID '{new_id}' with name '{new_name}'.")
        except Exception as e:
            print(f"Clone operation failed for ID {new_id}. Error: {e}")

    for new_id in new_vm_ids:
        print(f"Starting container {new_id}...")
        proxmox.nodes(node).lxc(new_id).status.start.post()
        print(f"Container {new_id} started successfully.")

    # Step 4: Retrieve the IP addresses of the new containers
    ip_addresses = []
    for new_id in new_vm_ids:
        # Wait a few seconds to allow the container to fully boot and retrieve its IP
        time.sleep(5)
        status = proxmox.nodes(node).lxc(new_id).status.current.get()
        # Extract the IP address
        ip_address = None
        if "data" in status and "ens18" in status['data']:
            ip_info = status['data']['net0'].get('ip-addresses', [])
            # Filter for a valid IPv4 address (not a link-local address)
            ip_address = next((ip['ip'] for ip in ip_info if ip['family'] == 'inet'), None)

        ip_addresses.append(ip_address)
        print(f"Container {new_id} has IP address: {ip_address}")

    return ip_addresses