from django.http.response import HttpResponse, JsonResponse
import json, requests

PFSENSE_HOST = 'http://192.168.1.1'
API_KEY = 'API_KEY'

def get_token():
    url = f"{PFSENSE_HOST}/api/v2/access_token"
    response = requests.post(url)
    return response

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
    try:
        # Example URL - replace with actual API call as needed
        response = requests.get('http://192.168.1.2:8000/api/get_rules')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        # Assuming the response is JSON and needs to be passed through
        return JsonResponse(response.json())
    except requests.RequestException as e:
        # Handles cases where the request itself failed
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        # General exception catch if something else went wrong
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)