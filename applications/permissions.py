from rest_framework import permissions

from users.models import UserProfile

class IsJobSeeker(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'job_seeker'
        except UserProfile.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            profile = UserProfile.objects.get(user=request.user)
            return obj.applicant == request.user and profile.role == 'job_seeker'
        except UserProfile.DoesNotExist:
            return False