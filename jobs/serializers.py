from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import JobPost
User = get_user_model()

class JobPostingSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    employer_name = serializers.ReadOnlyField(source='employer.username')

    class Meta:
        model = JobPost
        fields = ['id', 'title', 'type', 'description', 'salary_range', 'location', 'employer', 'employer_name', 'created_at']
        read_only_fields = ['id', 'employer', 'employer_name', 'created_at']
