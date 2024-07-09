from django.http.response import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import json, requests

PFSENSE_HOST = 'http://192.168.1.1'
API_KEY = '74c46c1735cc476bb78df2c189be73daf9753ba872d64f8'

def get_token():
    url = f"{PFSENSE_HOST}/api/v2/auth/key"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {}
    response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth("admin", "pfsense"))
    return response.json()

def add_firewall_rule():
    # url = f"{PFSENSE_HOST}/api/v2/firewall/apply"
    url = f"{PFSENSE_HOST}/api/v2/firewall/rule"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {API_KEY}"
    }

    data = {
        "interface": "wan",
        "protocol": "tcp/udp",
        "src": "any",
        "srcport": "",
        "dst": "wan_address",
        "dstport": "8000",
        "target": "192.168.1.2",
        "local-port": "8000",
        "descr": "Test",
        "natreflection": "enable",
        "noxmlrpc": 'false',
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    
def get_rules():
    token = get_token()
    url = f"{PFSENSE_HOST}/api/v2/firewall/nat/port_forwards"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)
    return response.json()