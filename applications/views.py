from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers

from .serializers import JobApplicationSerializer
from .models import JobApplication
from drf_spectacular.utils import extend_schema


class CreateApplication(ModelViewSet):

    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]


    @extend_schema(
        description="""
            This show the list of the job applications.
            - Job Seekers: Show their applications.
            - Employers: Show applications of their jobs.
        """,
        responses={200: JobApplicationSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



    @extend_schema(
        description="""
            This show the detail of the job application.
            - Job Seekers: Can only view their application.
            - Employers: Can only view application of their job.
        """,
        responses={200: JobApplicationSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



    @extend_schema(
        description="""
            Create a new job application.
            - Job Seekers: Can only create applications.
        """,
        responses={
            201: JobApplicationSerializer,
            400: 'Employer cannot create application.',
            401: 'Authentication credentials were not provided',
            500: 'Internal server error.(Can not apply same job twice )'
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="""
            Update the job application.(Full update is not allowed)
            - Job Seekers: Can only update cover letter of their own applications.
            - Employers: Can only update status of applications for their job posts.
        """,
        responses={
            200: JobApplicationSerializer,
            400: 'Only the applicant can change the cover letter.',
            404: 'No JobApplication matches the given query.'
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @extend_schema(
        description="""
            Update the job application.(Partial update is allowed)
            - Job Seekers: Can only update cover letter of their own applications.
            - Employers: Can only update status of applications for their job posts.
        """,
        responses={
            200: JobApplicationSerializer,
            400: 'You can not change the job post of the application or status of the application.',
            404: 'No JobApplication matches the given query.'
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @extend_schema(
        description="""
            Delete a job application.
            - Job Seekers: Can only delete their own applications.
            - Employers: Can only delete applications for their job posts.
            """,
        responses={
            204: None,
            404: 'No JobApplication matches the given query.'
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



    def get_queryset(self):
        """
        1. Job seekers can only view their applications.
        2. Employers can only view applications of their jobs.
        """
        user = self.request.user
        if user.profile.role == 'employer':
            return JobApplication.objects.filter(job_post__employer=user)
        return JobApplication.objects.filter(applicant=user)



    def perform_create(self, serializer):
        """
        This method is responsible to create a new application. It checks the following criteria:
        1. Employer cannot create an application.
        2. Status must be submitted.
        3. By default, status is set to 'submitted'.
        """
        user = self.request.user
        if user.profile.role == 'employer':
            raise serializers.ValidationError('Employer cannot create application.')

        if 'status' in serializer.validated_data.keys() and serializer.validated_data['status'] != 'submitted':
            raise serializers.ValidationError('Status must be submitted.')

        serializer.validated_data['status']  = 'submitted'
        serializer.save(applicant=self.request.user)


    def perform_update(self, serializer):
        """
        1. Only the applicant can change the cover letter.
        2. Only the employer can change the status
        """
        user = self.request.user
        instance = self.get_object()

        if user.profile.role == 'employer':
            if instance.job_post.employer != user:
                raise serializers.ValidationError('You are not the job poster of this application.')
            if 'cover_letter' in serializer.validated_data and instance.cover_letter != serializer.validated_data['cover_letter']:
                raise serializers.ValidationError('Only the applicant can change the cover letter.')

        if user.profile.role == 'job_seeker':
            if instance.applicant != user:
                raise serializers.ValidationError('Neither you are the owner of this application nor you are an employer of this job post.')
            if 'status' in serializer.validated_data  and instance.applicant == user and instance.status != serializer.validated_data['status']:
                raise serializers.ValidationError('You do not have permission to change the status of your application.')

        serializer.save()

