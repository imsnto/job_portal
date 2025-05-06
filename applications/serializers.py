from rest_framework import serializers
from django.contrib.auth import get_user_model

from applications.models import JobApplication
from jobs.models import JobPost

User = get_user_model()

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.ReadOnlyField(source='applicant.username')
    job_title = serializers.ReadOnlyField(source='job_post.title')
    job_post = serializers.PrimaryKeyRelatedField(queryset=JobPost.objects.all())

    class Meta:
        model = JobApplication
        fields = ['id','applicant', 'job_post', 'job_title', 'cover_letter', 'status', 'applied_at']

        read_only_fields = ('id', 'applicant', 'job_title', 'applied_at')



