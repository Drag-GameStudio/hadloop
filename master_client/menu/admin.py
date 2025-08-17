from django.contrib import admin
from .models import Client, File
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display=["ip",]

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display=["file_name",]

