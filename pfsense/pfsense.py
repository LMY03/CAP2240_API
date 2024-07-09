from django.http.response import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import json, requests

PFSENSE_HOST = 'http://192.168.1.1'
API_KEY = '74c46c1735cc476bb78df2c189be73daf9753ba872d64f8'

def get_token():
    url = f'{PFSENSE_HOST}/api/v2/auth/jwt'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth("admin", "pfsense"))
    print("----------------------")
    print(response.json())
    return response.json()['data']['token']

def apply_changes():
    token = get_token()
    url = f'{PFSENSE_HOST}/api/v2/firewall/apply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    response = requests.post(url, headers=headers)
    return response.json()['data']['token']

def add_firewall_rule(protocol, destination_port, ip_add, local_port):
    token = get_token()
    url = f'{PFSENSE_HOST}/api/v2/firewall/nat/port_forward'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    data = {
        'interface': 'wan',
        'protocol': protocol,
        'source': 'any',
        # 'source_port': 'any',
        'destination': 'wan:ip',
        'destination_port': destination_port,
        'target': ip_add,
        'local_port': local_port,
        'disabled': False,
        # 'nordr': True, # notsure
        # 'nosync': True,
        'descr': 'Test',
        'associated_rule_id': '',
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
    return response.json()['data']['id']

def edit_firewall_rule(id, ip_add):
    token = get_token()
    url = f'{PFSENSE_HOST}/api/v2/firewall/nat/port_forward'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    data = {
        'id': id,
        'target': ip_add,
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()

def delete_firewall_rule(rule_id):
    try:
        token = get_token()
        url = f'{PFSENSE_HOST}/api/v2/firewall/nat/port_forward?id={rule_id}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        print(f"Attempting to delete rule at: {url}")
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {'error': str(http_err)}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {'error': str(err)}


    
def get_rules():
    token = get_token()
    url = f"{PFSENSE_HOST}/api/v2/interfaces"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)
    return response.json()

# https://github.com/jaredhendrickson13/pfsense-api/blob/dbd61d89b93bb85eb64a4ed7b9f477729d8ea9cf/pfSense-pkg-RESTAPI/files/usr/local/pkg/RESTAPI/Models/PortForward.inc