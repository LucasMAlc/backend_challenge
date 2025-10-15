from django.contrib import admin
from .models import Career

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'username', 'created_datetime']
    list_filter = ['created_datetime', 'username']
    search_fields = ['title', 'content', 'username']
    readonly_fields = ['created_datetime']
    ordering = ['-created_datetime']