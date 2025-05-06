from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import JobPost
User = get_user_model()

class JobPostingSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = JobPost
        fields = ['title', 'type', 'description', 'salary_range', 'location', 'employer', 'created_at']
        read_only_fields = ('user', 'created_at')
