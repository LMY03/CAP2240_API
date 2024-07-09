from django.http.response import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import json, requests

PFSENSE_HOST = 'http://192.168.1.1'
API_KEY = '74c46c1735cc476bb78df2c189be73daf9753ba872d64f8'

def get_token():
    url = f"{PFSENSE_HOST}/api/v2/auth/jwt"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {}
    response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth("admin", "pfsense"))
    return response.json()['data']['token']

def add_firewall_rule():
    token = get_token()
    # url = f"{PFSENSE_HOST}/api/v2/firewall/apply"
    url = f"{PFSENSE_HOST}/api/v2/firewall/nat/port_forward"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    data = {
        'interface': 'wan',
        'protocol': 'tcp',
        'source': 'any',
        # 'source_port': 'any',
        'destination': 'wanip',
        'destination_port': '8080',
        'target': '192.168.1.100',
        'local_port': '80',
        'disabled': False,
        # 'nordr': True, # notsure
        # 'nosync': True,
        'descr': 'Test',
        'natreflection': 'enable',
        'associated_rule_id': '',
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['data']['id']

def edit_firewall_rule(id):
    token = get_token()
    url = f"{PFSENSE_HOST}/api/v2/firewall/nat/port_forward"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    data = {
        'id': id,
        'interface': 'wan',
        'protocol': 'tcp',
        'source': 'any',
        # 'source_port': 'any',
        'destination': 'wan',
        'destination_port': '8080',
        'target': '192.168.1.100',
        'local_port': '80',
        'disabled': False,
        # 'nordr': True, # notsure
        # 'nosync': True,
        'descr': 'Test',
        # 'natreflection': 'system',
        'associated_rule_id': '',
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()
    
def get_rules():
    token = get_token()
    url = f"{PFSENSE_HOST}/api/v2/interfaces"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)
    return response.json()