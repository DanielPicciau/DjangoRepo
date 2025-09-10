from django.contrib import admin
from .models import Client, AccessRequest


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone", "created_by", "created_at")
    list_filter = ("created_by", "created_at")
    search_fields = ("name", "company", "email", "phone")

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at", "responded_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)

# Register your models here..
