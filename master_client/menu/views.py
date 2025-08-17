from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Client, File
from settings.hadloop_settings import Settings
from files_handle.loader import send_file_to_client
import threading
import json

# Create your views here.
def render_menu(request):
    return render(request, "menu/menu.html")

def get_all_clients(request):
    all_clients = Client.objects.all()
    all_ips = [el.ip for el in all_clients]

    return JsonResponse({"all_ips": all_ips})

def add_new_client(request):
    data = json.loads(request.body)
    client_ip = data.get("client_ip")
    if Client.objects.filter(ip=client_ip).first() is None:
        Client.objects.create(ip=client_ip)
        return HttpResponse("client has been added")
    
    return HttpResponse("this client has been already added", status=400)

def upload_file(request):
    current_file = request.FILES.get("file")
    if current_file:
        send_file_to_client(current_file, str(current_file), Settings())
    return HttpResponse("")
    


