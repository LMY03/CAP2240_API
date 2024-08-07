import requests, time

# Parameters
PROXMOX_HOST = 'https://10.1.200.11:8006'
USERNAME = 'root@pam'
PASSWORD = 'cap2240'
CA_CRT = False # Disable SSL certificate verification / self-signed certificates
# CA_CRT = '/path/to/ca_bundle.crt'

def get_proxmox_ticket():
    url = f"{PROXMOX_HOST}/api2/json/access/ticket"
    data = { 'username': USERNAME, 'password': PASSWORD }
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

def get_task_status(node, upid):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/tasks/{upid}/status"
    session = get_authenticated_session()
    response = session.get(url)

    return response.json()

def get_qemu_status(node, vmid):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/agent/info"
    session = get_authenticated_session()
    response = session.get(url)

    return response.status_code

def get_vm_ip(node, vmid, port="ens18"):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces"
    session = get_authenticated_session()
    response = session.get(url)
    return response.json()

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

def wait_for_task(node, upid): 
    while True:
        task_status = get_task_status(node, upid)
        if task_status['data']['status'] == 'stopped':
            return task_status['data']['exitstatus'] # OK
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
                    print("interface")
                    if 'ip-addresses' not in interface: continue  
                    for ip in interface['ip-addresses']:
                        if ip['ip-address-type'] == 'ipv4':
                            return ip['ip-address']
        time.sleep(5)