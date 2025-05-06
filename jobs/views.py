from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from jobs.models import JobPosting
from jobs.serializers import JobPostingSerializer

from .permissions import IsEmployer

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsEmployer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'location']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


