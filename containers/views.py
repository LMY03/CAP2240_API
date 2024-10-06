from django.http import JsonResponse
from django.shortcuts import render, redirect
import time

from . import proxmox

# Create your views here.

def renders(request):
    return render(request, "containers/form.html")

def test(request):
    data = proxmox.get_ip_address("pve", 4003)
    return JsonResponse({"success": True, "data": data})

def clone_lxc(request):
    if request.method == "POST":

        data = request.POST
        vmid = [data.get("vmid")]
        newid = [data.get("newid")]

        vmid = 4000
        newid = [4003, 4004]
        newnames = ["container-1", "container-2"]

        data = mass_provision(vmid, newid, newnames)

        return render(request, "containers/data.html", { 'data' : data })
    
    # return redirect('containers:form')

def create_test_vm(request):

    lxc_template_id = 4000
    new_vm_id = 4001
    cpu_cores=2
    ram = 2048

    vm_name = "API-TEST-VM"
    node = "jin"
    proxmox.clone_lxc(node, lxc_template_id, new_vm_id, vm_name)
    proxmox.wait_for_clone_completion(node, new_vm_id)
    proxmox.config_lxc(node, new_vm_id, cpu_cores, ram)
    proxmox.start_lxc(node, new_vm_id)
    # ip_add = proxmox.wait_and_fetch_lxc_ip(node, new_vm_id)
    proxmox.shutdown_lxc(node, new_vm_id)
    proxmox.wait_for_lxc_stop(node, new_vm_id)

    # return JsonResponse({"success": True, "ip_add": ip_add})

def mass_provision(original_vm_id, new_vm_ids, new_vm_names):
    original_vm_id = int(original_vm_id)  # Ensure the original VM ID is an integer
    node = 'pve'  # Modify this as per your Proxmox node name

    # Loop through each new VM ID and Name to perform cloning sequentially
    for new_vm_id, new_vm_name in zip(new_vm_ids, new_vm_names):
        print(f"Starting clone operation for new container ID: {new_vm_id} with name: {new_vm_name}")

        # Wait for the template to be unlocked before starting the clone
        if not proxmox.wait_for_template_unlock(node, original_vm_id):
            print(f"Template {original_vm_id} did not unlock in time. Skipping clone for {new_vm_id}.")
            continue

        # Start the clone operation
        proxmox.clone_lxc(node, original_vm_id, new_vm_id, new_vm_name)

        # Wait for the cloning operation to complete
        proxmox.wait_for_clone_completion(node, new_vm_id)
        proxmox.config_lxc(node, new_vm_id, 1, 4096)
        proxmox.start_lxc(node, new_vm_id)

    print("All containers cloned successfully.")

    # # Wait until all clone operations are complete
    # while not all(proxmox.check_clone_status(node, vm_id) for vm_id in new_vm_ids):
    #     time.sleep(5)  # Check every 5 seconds

    # # Start all the cloned containers
    # for new_vm_id in new_vm_ids:
    #     proxmox.start_lxc(node, new_vm_id)

    # Retrieve IP addresses of the cloned containers
    ip_addresses = []
    max_retries = 10  # Maximum number of retries before timing out
    retry_delay = 5   # Delay in seconds between retries

    for new_vm_id, new_vm_name in zip(new_vm_ids, new_vm_names):
        # Retry mechanism to get the IP address
        for attempt in range(max_retries):
            ip_address = proxmox.get_ip_address(node, new_vm_id)
            if ip_address:
                ip_addresses.append(ip_address)
                print(f"Container {new_vm_name} (ID: {new_vm_id}) has IP address: {ip_address}")
                break
            else:
                print(f"Waiting for IP address for {new_vm_name} (ID: {new_vm_id}), attempt {attempt + 1}...")
                time.sleep(retry_delay)  # Wait before retrying
        else:
            # If IP address is not found after all retries, log a warning
            ip_addresses.append(None)
            print(f"Warning: Could not retrieve IP address for {new_vm_name} (ID: {new_vm_id}) after {max_retries} attempts.")

    for new_vm_id in new_vm_ids:
        proxmox.shutdown_lxc(node, new_vm_id)
        proxmox.wait_for_lxc_stop(node, new_vm_id)
        proxmox.delete_lxc(node, new_vm_id)

    print(ip_addresses)

    return JsonResponse({"success": True, "ip_addresses": ip_addresses})

# def mass_provision(original_vm_id, new_vm_ids, new_vm_names, snap_name):

#     node = 'pve'  # Assuming node is 'pve', modify as per your setup

#     # Step 1: Create a snapshot of the original container
#     snapshot_name = proxmox.create_snapshot(node, original_vm_id, snap_name)

#     # Step 2: Perform cloning for each VM ID and Name
#     for new_vm_id, new_vm_name in zip(new_vm_ids, new_vm_names):
#         proxmox.clone_container(node, original_vm_id, snapshot_name, new_vm_id, new_vm_name)

#     # Step 3: Wait for all clones to be completed
#     while not all(proxmox.check_clone_status(node, vm_id) for vm_id in new_vm_ids):
#         time.sleep(5)  # Check every 5 seconds

#     # Step 4: Start all the cloned containers
#     for new_vm_id in new_vm_ids:
#         proxmox.start_lxc(node, new_vm_id)

#     proxmox.delete_snapshot(node, original_vm_id, snap_name)

#     # Step 5: Retrieve IP addresses of the cloned containers
#     ip_addresses = []
#     max_retries = 10  # Maximum number of retries before timing out
#     retry_delay = 5   # Delay in seconds between retries

#     for new_vm_id, new_vm_name in zip(new_vm_ids, new_vm_names):
#         # Retry mechanism to get the IP address
#         for attempt in range(max_retries):
#             ip_address = proxmox.get_ip_address(node, new_vm_id)
#             if ip_address:
#                 ip_addresses.append(ip_address)
#                 print(f"Container {new_vm_name} (ID: {new_vm_id}) has IP address: {ip_address}")
#                 break
#             else:
#                 print(f"Waiting for IP address for {new_vm_name} (ID: {new_vm_id}), attempt {attempt + 1}...")
#                 time.sleep(retry_delay)  # Wait before retrying
#         else:
#             # If IP address is not found after all retries, log a warning
#             ip_addresses.append(None)
#             print(f"Warning: Could not retrieve IP address for {new_vm_name} (ID: {new_vm_id}) after {max_retries} attempts.")

#     return JsonResponse({"success": True, "ip_addresses": ip_addresses})