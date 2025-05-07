from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from jobs.models import JobPost
from jobs.serializers import JobPostingSerializer

from .permissions import IsEmployer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class JobPostingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing job posts.
        - Allows anyone to view job posts (list/retrieve).
        - Restricts create/update/delete actions to authenticated employers.
        - Supports filtering by type/location and searching by title/description.
    """
    queryset = JobPost.objects.all()
    serializer_class = JobPostingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'location']
    search_fields = ['title', 'description']

    @extend_schema(
        description="""
            Retrieve all job posts. Anyone can view.
            - Supports filtering by `type` and `location`.
            - Supports searching by `title` and `description`.
        """,
        responses={200: JobPostingSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @extend_schema(
        description="""
            Retrieve a single job post. 
            Anyone can view the job post.
        """,
        responses={
            200: JobPostingSerializer,
            404: OpenApiParameter(name="error", type=str, description="No JobPost matches the given query..."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        description="""
            Create a new job post. Only employers can create job posts.
                - The authenticated user is set as the employer.
                - Returns the created job post.
        """,
        responses={
            201: JobPostingSerializer,
            401: OpenApiParameter(name="error", type=str, description="Authentication credentials were not provided."),
            403: OpenApiParameter(name="error", type=str, description="You do not have permission to perform this action."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(
        description="""
            Only employers can partially update the job post.
        """,
        responses={
            200: JobPostingSerializer,
            403: "You do not have permission to perform this action.",
            404: "No JobPost matches the given query.",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @extend_schema(
        description="""
            Only employers can update the job post.
        """,
        responses={200: JobPostingSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @extend_schema(
        description="""
            Only employers can delete the job post.
        """,
        responses={
            204: None,
            401: "Authentication credentials were not provided.",
            403: "You do not have permission to perform this action",
            404: "No JobPost matches the given query."
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    def perform_create(self, serializer):
        """Set the current user as the employer"""
        serializer.save(employer=self.request.user)


    def get_permissions(self):
        """
            Return permissions based on the action.
            - list/retrieve: Allow anyone.
            - create/update/destroy: Require authenticated employer.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsEmployer()]


