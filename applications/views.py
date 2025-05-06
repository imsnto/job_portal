from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers

from .serializers import JobApplicationSerializer
from .models import JobApplication

class CreateApplication(ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'employer':
            return JobApplication.objects.filter(job_post__employer=user)
        return JobApplication.objects.filter(applicant=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.profile.role == 'employer':
            raise serializers.ValidationError('Employer cannot create application.')
        serializer.save(applicant=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.profile.role == 'employer' and  self.get_object().job_post.employer != user:
            raise serializers.ValidationError('You do not have permission to change this application.')

        if user.profile.role == 'job_seeker' and instance.applicant == user and instance.status != serializer.validated_data['status']:
            raise serializers.ValidationError('You do not have permission to change the status of your application.')

        if user.profile.role == 'job_seeker' and instance.applicant != user:
            raise serializers.ValidationError('Neither you are the owner of this application nor you are an employer of this job post.')
        serializer.save()

