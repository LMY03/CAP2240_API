#!/usr/bin/env python
import json

# Example data that mimics pulling data from a dynamic source
hosts_data = [
    {"ip": "192.168.254.152", "ansible_user": "jin", "hostname": "Node_2", "label": "S12"},
    {"ip": "192.168.254.153", "ansible_user": "jin", "hostname": "Node_3", "label": "S13"}
]

# The JSON structure expected by Ansible
inventory = {
    "test": {
        "hosts": [],
        "vars": {}
    },
    "_meta": {
        "hostvars": {}
    }
}

for host in hosts_data:
    # Append IP addresses under the 'test' group
    inventory['test']['hosts'].append(host['ip'])
    # Add variables specific to each host
    inventory["_meta"]["hostvars"][host['ip']] = {
        "ansible_user": host['ansible_user'],
        "hostname": host['hostname'],
        "label": host['label']
    }

print(json.dumps(inventory))
