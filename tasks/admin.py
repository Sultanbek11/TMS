from django.contrib import admin
from .models import Task

@admin.register(Task)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'due_date', 'created_at')
