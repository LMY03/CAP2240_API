from django.http import JsonResponse
from django.shortcuts import render, redirect
import time

from . import proxmox

# Create your views here.

def renders(request) : 
    return render(request, "containers/form.html")

def clone_lxc(request):
    if request.method == "POST":

        data = request.POST
        vmid = [data.get("vmid")]
        newid = [data.get("newid")]

        vmid = 4002
        newid = [4003, 4004]
        newnames = ["container_1", "container_2"]

        data = mass_provision(vmid, newid, newnames)

        return render(request, "containers/data.html", { 'data' : data })
    
    # return redirect('containers:form')

def mass_provision(original_vm_id, new_vm_ids, new_vm_names):
    original_vm_id = int(original_vm_id)
    node = 'pve'  # Assuming node is 'pve', modify as per your setup

    # Convert the original container to a template
    # proxmox.convert_to_template(node, original_vm_id)

    # Perform cloning for each new VM ID and Name
    for new_vm_id, new_vm_name in zip(new_vm_ids, new_vm_names):
        print(f"Starting clone operation for new container ID: {new_vm_id} with name: {new_vm_name}")
        proxmox.clone_lxc(node, original_vm_id, new_vm_id, new_vm_name)

    # Wait until all clone operations are complete
    while not all(proxmox.check_clone_status(node, vm_id) for vm_id in new_vm_ids):
        time.sleep(5)  # Check every 5 seconds

    # Start all the cloned containers
    for new_vm_id in new_vm_ids:
        proxmox.start_lxc(node, new_vm_id)

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