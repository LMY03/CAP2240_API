"""
URL configuration for CAP2240_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import path

from django.shortcuts import render

def tsg_home(request):
    return render(request, 'monitoring/tsg_home.html')

urlpatterns = [
    path('guacamole/', include("guacamole.urls")),
    path('pfsense/', include("pfsense.urls")),
    path('proxmox/', include("proxmox.urls")),
    path('ticketing/', include("ticketing.urls")),
    path('admin/', admin.site.urls),
    path('monitoring/', include('monitoring.urls')),
    path('dashboard', tsg_home)
]