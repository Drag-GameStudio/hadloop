from django.urls import path
from .views import render_manager, get_all_files, delete_file_view, download_file, upload_and_run_zip

urlpatterns = [
    path("/", render_manager),
    path("get_files", get_all_files),
    path("delete_file", delete_file_view),
    path("download_file", download_file),
    path("upload_and_run/<str:file_name>", upload_and_run_zip)
]