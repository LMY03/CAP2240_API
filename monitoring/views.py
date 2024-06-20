from django.shortcuts import render
import requests

# Create your views here.

# def renders(request) : 
#     ip_add = {
#         "192.168.254.165",
#         "192.168.254.166",
#     }
#     # template = "monitoring.html"
#     template = "index.html"
#     return render(request, template, { "ip_add" : ip_add })

def fetch_netdata_metrics():
    base_url = "http://192.168.254.162:19999/api/v1/data?chart={chart}&format=json"
    charts = {
        'cpu': 'system.cpu',
        'memory': 'system.ram',
        'network': 'system.net'
    }
    data = {}
    for key, chart in charts.items():
        response = requests.get(base_url.format(chart=chart))
        if response.status_code == 200:
            data[key] = response.json()
        else:
            data[key] = {}
    return data

def renders(request):
    data = fetch_netdata_metrics()
    return render(request, 'index.html', {'data': data})
