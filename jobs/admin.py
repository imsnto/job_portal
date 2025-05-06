from django.contrib import admin
from .models import JobPost

@admin.register(JobPost)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'salary_range', 'location', 'employer')
