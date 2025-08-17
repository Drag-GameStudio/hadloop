from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from menu.models import File
from files_handle.loader import delete_file, get_full_file, run_script_on_file
import json
# Create your views here.
def render_manager(request):
    return render(request, "files_manager/files_manager.html")

def get_all_files(request):
    files_name = [[el.file_name, el.is_ready] for el in File.objects.all()]
    return JsonResponse({"files_name": files_name})

def delete_file_view(request):
    file_name = json.loads(request.body).get("file_name")
    delete_file(file_name)
    return HttpResponse("file was deleted")

def download_file(request):
    file_name = request.GET.get("file_name")
    full = get_full_file(file_name)
    

    response = HttpResponse(full, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def upload_and_run_zip(request, file_name):
    if request.method == "POST":
        file = request.FILES.get('file')
        result = run_script_on_file(file_name, file)
        return JsonResponse({"result": result})