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

def convert_to_template(node, vm_id):
    print(f"Converting container {vm_id} to a template...")
    get_proxmox_client().nodes(node).lxc(vm_id).template().create()
    print(f"Container {vm_id} has been converted to a template.")

    wait_for_template_conversion(node, vm_id)

def wait_for_template_conversion(node, vm_id, timeout=300, interval=5):
    """Wait until the container is successfully converted to a template."""
    print(f"Waiting for container {vm_id} to complete template conversion...")
    total_time = 0
    while total_time < timeout:
        # Check the current status of the container
        config = get_proxmox_client().nodes(node).lxc(vm_id).status.current().get()
        if config.get('template', 0) == 1:  # 'template' field becomes 1 when it's a template
            print(f"Container {vm_id} is now a template.")
            return True
        print(f"Container {vm_id} is still converting to a template, waiting...")
        time.sleep(interval)
        total_time += interval
    raise TimeoutError(f"Container {vm_id} did not convert to a template after {timeout} seconds.")

def create_snapshot(node, vm_id, snapshot_name="automation_snapshot"):
    get_proxmox_client().nodes(node).lxc(vm_id).snapshot().create(snapname=snapshot_name)
    return snapshot_name

def delete_snapshot(node, vm_id, snapshot_name):
    get_proxmox_client().nodes(node).lxc(vm_id).snapshot(snapshot_name).delete()

def clone_container(node, vm_id, snapshot, new_vm_id, new_vm_name):
    wait_for_unlock(node, vm_id)
    get_proxmox_client().nodes(node).lxc(vm_id).clone().create(
        newid=new_vm_id,
        hostname=new_vm_name,
        full=1,
        snapname=snapshot
    )

def clone_lxc(node, template_id, new_vm_id, new_vm_name):
    print(f"Cloning new container {new_vm_id} ({new_vm_name}) from template {template_id}...")
    get_proxmox_client().nodes(node).lxc(template_id).clone().create(
        newid=new_vm_id,
        hostname=new_vm_name,
        full=1,
    )
    print(f"Clone {new_vm_id} ({new_vm_name}) created successfully.")

def shutdown_lxc(node, vm_id):
    get_proxmox_client().nodes(node).lxc(vm_id).status.shutdown().post()

def stop_lxc(node, vm_id):
    get_proxmox_client().nodes(node).lxc(vm_id).status.stop().post()

def delete_lxc(node, vm_id):
    get_proxmox_client().nodes(node).lxc(vm_id).delete()

# # configure VM PUT 
def config_lxc(node, vm_id, cpu_cores, memory_mb):
    get_proxmox_client().nodes(node).lxc(vm_id).config.put(
        cores=cpu_cores,
        memory=memory_mb,
    )

def get_lxc_status(node, vm_id):
    return get_proxmox_client().nodes(node).lxc(vm_id).status.current().get()

def is_template_locked(node, vm_id):
    """
    Check if the template or container is locked.
    :param node: Proxmox node name.
    :param vm_id: ID of the VM or container.
    :return: True if locked, False otherwise.
    """
    # Query the status of the template/container
    status = get_proxmox_client().nodes(node).lxc(vm_id).status.current().get()
    return 'lock' in status

def wait_for_template_unlock(node, vm_id, timeout=300, interval=5):
    """
    Wait until the template is unlocked.
    :param node: Proxmox node name.
    :param vm_id: ID of the template/container.
    :param timeout: Maximum time to wait (in seconds).
    :param interval: Time interval between checks (in seconds).
    :return: True if unlocked within timeout, False otherwise.
    """
    total_time = 0
    while total_time < timeout:
        # Check if the template is locked
        if not is_template_locked(node, vm_id):
            print(f"Template {vm_id} is now unlocked and ready for cloning.")
            return True
        else:
            print(f"Template {vm_id} is currently locked. Waiting for it to be unlocked...")
        
        # Wait for the next interval before checking again
        time.sleep(interval)
        total_time += interval
    
    print(f"Template {vm_id} is still locked after {timeout} seconds. Exiting.")
    return False

def wait_for_clone_completion(node, new_vm_id, timeout=300, interval=5):
    """
    Wait for a container clone operation to complete, considering config lock status.
    
    :param node: The Proxmox node name.
    :param new_vm_id: The ID of the new cloned container.
    :param timeout: Total time in seconds to wait for the clone to complete.
    :param interval: Time in seconds between status checks.
    :return: True if clone completed successfully, False if timeout reached.
    """
    total_wait_time = 0
    while total_wait_time < timeout:
        # Check the status of the container
        status = get_proxmox_client().nodes(node).lxc(new_vm_id).status.current().get()
        print(status)
        print(f"Checking status of container {new_vm_id}: {status['status']} (Config: {status.get('lock', 'None')})")

        # If the container is not locked, the cloning operation is complete
        if 'lock' not in status:
            print(f"Container {new_vm_id} clone operation completed successfully.")
            return True

        # If the container is locked for creation, continue waiting
        if status.get('lock') == 'create':
            print(f"Container {new_vm_id} is still being cloned. Waiting...")

        # Wait for the next interval before checking again
        time.sleep(interval)
        total_wait_time += interval

    # If we reach here, the cloning operation did not complete within the timeout
    print(f"Timeout reached while waiting for clone {new_vm_id} to complete.")
    return False


def wait_for_unlock(node, vm_id, timeout=300, interval=5):
    total_time = 0
    while total_time < timeout:
        # Check if the container is locked
        config = get_proxmox_client().nodes(node).lxc(vm_id).status.current().get()
        if 'lock' not in config:
            return True  # Unlocked, proceed with the next step
        print(f"Container {vm_id} is locked, waiting...")
        time.sleep(interval)  # Wait before the next check
        total_time += interval
    raise TimeoutError(f"Container {vm_id} is still locked after {timeout} seconds.")

def check_clone_status(node, vm_id):
    task_status = get_proxmox_client().nodes(node).tasks().get()
    for task in task_status:
        if task['upid'].startswith(f"UPID:{node}:{vm_id}:") and task['status'] == 'running':
            return False
    return True

def start_lxc(node, vm_id):
    get_proxmox_client().nodes(node).lxc(vm_id).status.start().post()


def get_ip_address(node, vm_id):
    network_info = get_proxmox_client().nodes(node).lxc(vm_id).interfaces().get()
    print(network_info)
    if network_info:
        for interface in network_info:
            if interface['name'] == "eth0":
                if 'inet' in interface:
                    return interface['inet'].split('/')[0]

def wait_for_lxc_stop(node, vmid):
    while True:
        status = get_lxc_status(node, vmid).get('status')
        if status == "stopped" : return status
        time.sleep(5)

# def clone_lxc(node, vm_id, new_vm_ids, new_names):
#     # Initialize Proxmox API connection
#     proxmox = ProxmoxAPI('10.1.200.11', user='root@pam', password='cap2240', verify_ssl=False)

#     for new_id, new_name in zip(new_vm_ids, new_names):
#         try:
#             print(f"Starting clone operation for new container ID: {new_id} with name: {new_name}")
            
#             # Perform the clone operation
#             task = proxmox.nodes(node).lxc(vm_id).clone.post(
#                 newid=new_id,
#                 target=node,
#                 full=1,
#                 storage='local-lvm',
#             )
#             print(f"Successfully cloned LXC ID '{vm_id}' to new ID '{new_id}'.")

#             # Use config.put to clear the lock instead of status.unlock.post
#             print(f"Clearing the lock for the cloned container {new_id}...")
#             proxmox.nodes(node).lxc(new_id).config.put(
#                 lock=None
#             )
#             print(f"Container {new_id} lock cleared successfully.")

#             # Optional: Start the container if needed
#             print(f"Starting container {new_id}...")
#             proxmox.nodes(node).lxc(new_id).status.start.post()
#             print(f"Container {new_id} started successfully.")

#         except Exception as e:
#             print(f"Clone operation failed for ID {new_id}. Error: {e}")

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
