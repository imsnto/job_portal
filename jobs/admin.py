from django.contrib import admin
from .models import JobPosting

@admin.register(JobPosting)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'salary_range', 'location', 'user')
