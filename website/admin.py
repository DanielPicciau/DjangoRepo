from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone", "created_by", "created_at")
    list_filter = ("created_by", "created_at")
    search_fields = ("name", "company", "email", "phone")

# Register your models here..
