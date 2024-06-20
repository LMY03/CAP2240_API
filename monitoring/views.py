from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

# Create your views here.

# def renders(request) : 
#     ip_add = {
#         "192.168.254.165",
#         "192.168.254.166",
#     }
#     # template = "monitoring.html"
#     template = "index.html"
#     return render(request, template, { "ip_add" : ip_add })

# def fetch_netdata_metrics():
#     base_url = "http://192.168.254.162:19999/api/v1/data?chart={chart}&format=json"
#     charts = {
#         'cpu': 'system.cpu',
#         'memory': 'system.ram',
#         'network': 'system.net'
#     }
#     data = {}
#     for key, chart in charts.items():
#         response = requests.get(base_url.format(chart=chart))
#         if response.status_code == 200:
#             data[key] = response.json()
#         else:
#             data[key] = {}
#     return data

# def renders(request):
#     data = fetch_netdata_metrics()
#     return render(request, 'index.html', {'data': data})

# def fetch_netdata_metrics():
#     base_url = "http://192.168.254.162:19999/api/v1/data?chart={chart}&format=json"
#     charts = {
#         'cpu': 'system.cpu',
#         'memory': 'system.ram',
#         'network': 'system.net'
#     }
#     data = {}
#     for key, chart in charts.items():
#         response = requests.get(base_url.format(chart=chart))
#         if response.status_code == 200:
#             chart_data = response.json()
#             data[key] = {
#                 'labels': list(range(len(chart_data['data']))),  # Use a range as labels
#                 'data': [sum(point) for point in chart_data['data']]  # Sum the data points for simplicity
#             }
#         else:
#             data[key] = {'labels': [], 'data': []}
#     return data

# def netdata_view(request):
#     data = fetch_netdata_metrics()
#     return render(request, 'netdata.html', {'data': json.dumps(data)})  # Use json.dumps to pass data as JSON

# def netdata_metrics_api(request):
#     data = fetch_netdata_metrics()
#     return JsonResponse(data)  # Return data as JSON response for AJAX requests

def index(request):
    return render(request, 'index.html')