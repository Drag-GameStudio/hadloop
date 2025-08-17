from django.urls import path
from .views import upload_file, delete_file, get_block, run_script

urlpatterns = [
    path("upload", upload_file),
    path("delete", delete_file),
    path("", get_block),
    path("run_script", run_script)
]