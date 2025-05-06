from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import JobPosting
User = get_user_model()

class JobPostingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = JobPosting
        fields = ['title', 'type', 'description', 'salary_range', 'location', 'user', 'created_at']
        read_only_fields = ('user', 'created_at')
