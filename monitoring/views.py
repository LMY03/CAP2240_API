from django.shortcuts import render
from django_tables2 import RequestConfig
import requests
from .tables import VMTable

def fetch_netdata_metrics(vm_url):
    # Replace with your actual endpoint and processing
    response = requests.get(f'http://{vm_url}/api/v1/allmetrics')
    data = response.json()
    
    # Extract CPU, memory, and network usage from data
    cpu = data['system.cpu']['value']
    memory = data['system.ram']['value']
    network = data['system.network']['value']
    
    return {
        'cpu': cpu,
        'memory': memory,
        'network': network,
    }

def vm_monitoring(request):
    vm_urls = [
        "192.168.254.162",
        "192.168.254.165",
    ]
    vms_data = []

    for vm_url in vm_urls:
        metrics = fetch_netdata_metrics(vm_url)
        vms_data.append({
            'name': vm_url,
            'cpu': metrics['cpu'],
            'memory': metrics['memory'],
            'network': metrics['network'],
        })

    table = VMTable(vms_data)
    RequestConfig(request).configure(table)
    return render(request, 'monitoring/vm_monitoring.html', {'table': table})
