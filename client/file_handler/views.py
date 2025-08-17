from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from file_handle.client_part import ClientLoader
from settings.hadloop_settings import Settings
from script_handler.handler import ScriptHandler
import os
# Create your views here.

@csrf_exempt
def upload_file(request):
    block = request.FILES.get("file")
    
    cl = ClientLoader(Settings())
    cl.save_block(block.read(), str(block))
    return HttpResponse("file was upload")

@csrf_exempt
def delete_file(request):
    file_name = request.POST.get("file_name")
    cl = ClientLoader(Settings())
    cl.delete_block(file_name)
    return HttpResponse("file hs been deleted")

@csrf_exempt
def get_block(request):
    file_name = request.GET.get("file_name")
    cl = ClientLoader(Settings())

    block_bytes = cl.get_block(file_name)
    encoded = base64.b64encode(block_bytes).decode('utf-8')

    return JsonResponse({"block": encoded})

@csrf_exempt
def run_script(request):

    file_name = request.POST.get("file_name")
    script_file = request.FILES.get("script_file")
    
    if os.path.isfile("script_handler/all_scripts/" + str(script_file)) == False: # подумать как заменять скрипты
        with open("script_handler/all_scripts/" + str(script_file), "wb") as f:
            f.write(script_file.read())

    cl = ClientLoader(Settings())
    block_bytes = cl.get_block(file_name)
    
    print(f"Run script on {file_name} for file {script_file}")
    sh = ScriptHandler("script_handler/all_scripts/" + str(script_file))
    result = sh.client_part(block_bytes)
    return JsonResponse({"result": result})