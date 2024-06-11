from django.shortcuts import render

# Create your views here.

def renders(request) : 
    return render(request, "ansible.html")

def run(request):
    return render(request, "ansible.html")
    # if request.method == "POST":
