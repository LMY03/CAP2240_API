from decouple import config
import requests, asyncio, time

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXMOX_HOST = config('PROXMOX_HOST')
USERNAME = config('PROXMOX_USERNAME')
PASSWORD = config('PROXMOX_PASSWORD')
# CA_CRT = config('CA_CRT')
CA_CRT = False

# def get_proxmox_ticket():
#     url = f"{PROXMOX_HOST}/api2/json/access/ticket"
#     data = { 'username': USERNAME, 'password': PASSWORD }
#     response = requests.post(url, data=data, verify=CA_CRT)
#     if response.status_code != 200:
#         time.sleep(5)
#         return get_proxmox_ticket()
#     return response.json()['data']['CSRFPreventionToken']

# # Authenticate
# def get_authenticated_session():
#     data = get_proxmox_ticket()
#     session = requests.Session()
#     session.verify = CA_CRT
#     session.headers.update({
#         'CSRFPreventionToken': data['data']['CSRFPreventionToken'],
#         'Authorization': f"PVEAuthCookie={data['data']['ticket']}",
#         # 'Cookie': f"PVEAuthCookie={data['data']['ticket']}",
#     })
#     return session

def get_ticket():
    url = f"{PROXMOX_HOST}/api2/json/access/ticket"
    data = { 'username': USERNAME, 'password': PASSWORD }
    
    try:
        response = requests.post(url, data=data, verify=CA_CRT, timeout=10)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"Error getting ticket: {e}")
        time.sleep(5)
        return get_ticket()
    
def get_headers():
    token = get_ticket()
    return {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }

def get_task_status(node, upid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/tasks/{upid}/status"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.get(url, headers=headers, verify=CA_CRT, timeout=10)
    if response.status_code != 200 : return get_task_status(node, upid)
    return response.json()

def get_qemu_status(node, vmid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/agent/info"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.get(url, headers=headers, verify=CA_CRT)

    return response.status_code

def get_vm_ip(node, vmid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.get(url, headers=headers, verify=CA_CRT)
    return response.json()

# get VM status
def get_vm_status(node, vmid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/current"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.get(url, headers=headers, verify=CA_CRT)

    status = response.json()['data']['qmpstatus']

    return status

def get_token_sync():
    return get_ticket()

def clone_vm(node, vmid, newid, name):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/clone"
    config = {
        'newid': newid,
        'full': 1,
        'name': name,
        # 'target': ''
        # 'storage': 'local-lvm',
    }
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.post(url, headers=headers, data=config, verify=CA_CRT)
    if response.status_code != 200 : return clone_vm(node, vmid, newid, name)

    return response.json()['data']

# delete VM DELETE
def delete_vm(node, vmid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.delete(url, headers=headers, verify=CA_CRT)
    if response.status_code != 200 : return delete_vm(node, vmid)
    return response.json()

# start VM POST
def start_vm(node, vmid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/start"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.post(url, headers=headers, verify=CA_CRT)
    return response.json()

# shutdown VM POST
def shutdown_vm(node, vmid):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/shutdown"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.post(url, headers=headers, verify=CA_CRT)
    return response.json()

# stop VM POST - only on special occasion like the vm get stuck
def stop_vm(node, vmid):              
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/status/stop"
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.post(url, headers=headers, verify=CA_CRT)
    return response.json()

# configure VM PUT 
def config_vm(node, vmid, cpu_cores, memory_mb):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/config"
    config = {
        'cores': cpu_cores,
        'memory': memory_mb,
    }
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.put(url, headers=headers, data=config, verify=CA_CRT)
    if response.status_code != 200 : return config_vm(node, vmid, cpu_cores, memory_mb)
    return response.json()

def config_vm_disk(node, vmid, size):
    token = get_ticket()
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/resize"
    config = {
        'disk': 'scsi0',
        'size': size,
    }
    headers = {
        'CSRFPreventionToken': token['CSRFPreventionToken'],
        'Cookie': f"PVEAuthCookie={ token['ticket'] }",
    }
    response = requests.put(url, headers=headers, data=config, verify=CA_CRT)
    return response.json()

def wait_for_task(node, upid):
    while True:
        task_status = get_task_status(node, upid)
        if task_status['data']['status'] == 'stopped' : return task_status['data']['exitstatus'] # OK
        time.sleep(5)

def wait_for_vm_start(node, vmid):
    while True:
        status = get_vm_status(node, vmid)
        if status == "running" : return status
        time.sleep(5)

def wait_for_vm_stop(node, vmid):
    while True:
        status = get_vm_status(node, vmid)
        if status == "stopped" : return status
        time.sleep(5)

def wait_and_get_ip(node, vmid):
    while True:
        response = get_vm_ip(node, vmid)
        if response['data'] != None :
            for interface in response['data']['result']:
                if interface['name'] == "ens18":
                    if 'ip-addresses' not in interface: continue  
                    for ip in interface['ip-addresses']:
                        if ip['ip-address-type'] == 'ipv4':
                            return ip['ip-address']
        time.sleep(5)
