import requests
from django.http import JsonResponse

# Parameters
PROXMOX_HOST = 'https://10.1.200.11:8006'
USERNAME = 'root@pam'
PASSWORD = 'cap2240'
CA_CRT = False # Disable SSL certificate verification / self-signed certificates
# CA_CRT = '/path/to/ca_bundle.crt'

def get_proxmox_ticket():
    url = f"{PROXMOX_HOST}/api2/json/access/ticket"
    data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    response = requests.post(url, data=data, verify=CA_CRT)  
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Authenticate
def get_authenticated_session():
    data = get_proxmox_ticket()
    session = requests.Session()
    session.verify = CA_CRT
    session.headers.update({
        'CSRFPreventionToken': data['data']['CSRFPreventionToken'],
        'Authorization': f"PVEAuthCookie={data['data']['ticket']}",
        # 'Cookie': f"PVEAuthCookie={data['data']['ticket']}",
    })
    return session

def get_vm_ip(node, vmid, port="ens18"):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces"
    session = get_authenticated_session()
    response = session.get(url)
    response.raise_for_status()

    ip_address = None
    for interface in response.json()['data']['result']:
        if interface['name'] == port:
            for ip in interface['ip-addresses']:
                if ip['ip-address-type'] == 'ipv4':
                    ip_address = ip['ip-address']
                    break

    if ip_address is None: return 
        # return JsonResponse({'error': 'IPv4 address not found for interface ens18'}, status=404)

    return ip_address

# get VM status
def get_vm_status(node, vmid):
    session = get_authenticated_session()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/current"
    response = session.get(url)
    response.raise_for_status()

    status = response.json()['data']['qmpstatus']

    return status

# clone VM POST
# TODO: how to keep track on the available vmid, need new name
# TODO: need to make sure there are enough disk space in the server before cloning the machine
def clone_vm(node, vmid, newid):                    
    session = get_authenticated_session()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/clone"
    config = {
        'newid': newid,
        'full': 1,
        # 'name': name,
        # 'target': ''
        # 'storage': 'local-lvm',
    }
    response = session.post(url, data=config)
    return response.json()


# delete VM DELETE
def delete_vm(node, vmid):
    session = get_authenticated_session()
    # shutdown vm before deleting them
    #   1. check status
    #   2. if status is running -> shutdown (response['data']['qmpstatus'] = running) 
    #   3. wait for it to shut down
    stop_vm(node, vmid)

    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}"
    response = session.delete(url)
    return response.json()

# start VM POST
def start_vm(node, vmid):
    session = get_authenticated_session()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/start"
    response = session.post(url)
    return response.json()

# shutdown VM POST
def shutdown_vm(node, vmid):
    session = get_authenticated_session()
    node = "pve"
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/shutdown"
    response = session.post(url)
    return response.json()

# stop VM POST - only on special occasion like the vm get stuck
def stop_vm(node, vmid):              
    session = get_authenticated_session()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/stop"
    response = session.post(url)
    return response.json()

# configure VM PUT 
def config_vm(node, vmid, cpu_cores, memory_mb):
    session = get_authenticated_session()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/config"
    config = {
        'cores': cpu_cores,
        'memory': memory_mb,
    }
    response = session.put(url, data=config)
    return response.json()

# get vm ip # TODO: have not test yet
# def get_vm_ip(node, vmid):
#     url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces"
#     # headers = {
#     #     'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
#     #     'CSRFPreventionToken': 'YOUR_CSRF_TOKEN'
#     # }
#     # response = requests.get(url, headers=headers, verify=False)  # Verify should ideally be True in production
#     response = requests.get(url, verify=False)
#     data = response.json()
#     # Parsing the response to extract IP addresses
#     if 'result' in data:
#         interfaces = data['result']
#         for interface in interfaces:
#             if 'ip-addresses' in interface:
#                 for ip in interface['ip-addresses']:
#                     if ip['ip-address-type'] == 'ipv4':  # or ipv6 if you prefer
#                         return ip['ip-address']
#     return "No IP address found"
