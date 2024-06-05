from django.shortcuts import redirect, render
from . import guacamole

# Create your views here.

def guacamole_render(request) : 
    return render(request, "ticketing/guacamole.html")

def guacamole_submit(request) : 
    if request.method == "POST":

        data = request.POST
        username = data.get("username")
        password = data.get("password")
        guacamole.create_user(username, password)
        return redirect("home")
    return redirect("home")
