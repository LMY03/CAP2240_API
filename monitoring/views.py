from django.shortcuts import render
from django_tables2 import RequestConfig
import requests
from requests.exceptions import RequestException
from .tables import VMTable

def fetch_netdata_metrics(vm_url):
    try:
        response = requests.get(f'http://{vm_url}:19999/api/v1/allmetrics?format=json')
        response.raise_for_status()
        data = response.json()
        
        # Debug: Print the top-level keys
        print(f"Top-level keys: {list(data.keys())}")
        
        # You need to identify the exact paths to the metrics you need
        # Example paths (replace these with actual paths from your Netdata setup)
        cpu_key = 'system.cpu'
        memory_key = 'system.ram'
        network_key = 'system.network'

        # Assuming each metric is under a 'value' key within its dictionary
        cpu = data.get(cpu_key, {}).get('value', 'N/A')
        memory = data.get(memory_key, {}).get('value', 'N/A')
        network = data.get(network_key, {}).get('value', 'N/A')

        return {
            'cpu': cpu,
            'memory': memory,
            'network': network,
        }
    except RequestException as e:
        print(f"Error fetching data from {vm_url}: {e}")
        return {
            'cpu': 'N/A',
            'memory': 'N/A',
            'network': 'N/A',
        }
    except KeyError as e:
        print(f"KeyError: {e} in data: {data}")
        return {
            'cpu': 'N/A',
            'memory': 'N/A',
            'network': 'N/A',
        }

def vm_monitoring(request):
    vm_urls = ["192.168.254.165", "192.168.254.166"]  # Replace with actual VM addresses
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
    return render(request, 'vm_monitoring.html', {'table': table})
