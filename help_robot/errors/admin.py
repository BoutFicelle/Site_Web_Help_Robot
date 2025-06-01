# errors/admin.py
from django.contrib import admin
from .models import Brand, ErrorCodeFanuc

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']

@admin.register(ErrorCodeFanuc)
class ErrorCodeFanucAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['code', 'title', 'cause_en', 'cause_fr']
    readonly_fields = ['created_at']