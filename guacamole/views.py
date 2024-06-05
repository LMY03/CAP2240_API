from django.shortcuts import redirect, render
from . import guacamole

# Create your views here.

def render(request) : 
    return render(request, "guacamole/guacamole.html")

def success(request) : 
    return render(request, "guacamole/success.html")

def create_user(request) : 
    if request.method == "POST":

        data = request.POST
        username = data.get("username")
        password = data.get("password")
        guacamole.create_user(username, password)
        return redirect("/guacamole/success")
    return redirect("/guacamole")
