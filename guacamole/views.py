from django.shortcuts import redirect, render

from . import guacamole

# Create your views here.

parent_identifier = "ROOT"

def renders(request) : 
    return render(request, "guacamole.html")

def success(request) : 
    return render(request, "success.html")

def create_user(request) : 

    if request.method == "POST":

        data = request.POST
        username = data.get("username")
        password = data.get("password")

        guacamole.create_user(username, password)

        return redirect("/guacamole/success")
    
    return redirect("/guacamole")

def delete_user(request) : 

    if request.method == "POST":

        data = request.POST
        username = data.get("username")

        guacamole.delete_user(username)

        return redirect("/guacamole/success")
    
    return redirect("/guacamole")

def create_connection(request) : 

    if request.method == "POST":

        data = request.POST
        name = data.get("name")
        protocol = data.get("protocol")
        hostname = data.get("hostname")
        username = data.get("username")
        password = data.get("password")

        port = {
            'vnc': 5901,
            'rdp': 3389,
            'ssh': 22
        }.get(protocol)

        connection_id = guacamole.create_connection(name, protocol, port, hostname, username, password, parent_identifier)

        return render(request, "connection_id.html", { "connection_id" : connection_id })
    
    return redirect("/guacamole")

def delete_connection(request) : 

    if request.method == "POST":

        data = request.POST
        connection_id = data.get("connection_id")

        guacamole.delete_connection(connection_id)

        return redirect("/guacamole/success")
    
    return redirect("/guacamole")


def assign_connection(request) : 

    if request.method == "POST":

        data = request.POST
        connection_id = data.get("connection_id")

        guacamole.delete_connection(connection_id)

        return redirect("/guacamole/success")
    
    return redirect("/guacamole")
