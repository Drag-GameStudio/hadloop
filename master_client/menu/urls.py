from django.urls import path
from .views import render_menu, get_all_clients, add_new_client, upload_file

urlpatterns = [
    path("/", render_menu),
    path("add_client", add_new_client),
    path("get_clients", get_all_clients),
    path("upload_file", upload_file)
]