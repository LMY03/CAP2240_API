from django.http.response import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import json, requests

PFSENSE_HOST = 'http://192.168.1.1'
API_KEY = 'a0762d86ae7aa908e23ffea953d1a4f9'

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
    url = f"{PFSENSE_HOST}/api/v2/firewall/nat/port_forwards"  # Adjust this endpoint as needed
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Checks for HTTP request errors
        return response.json()  # Returns the JSON response from the API
    except requests.RequestException as e:
        return {'error': str(e)}