from rest_framework import permissions

from users.models import UserProfile

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = UserProfile.objects.get(user=request.user)
            return  profile.role == 'employer'
        except UserProfile.DoesNotExist as e:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            profile = UserProfile.objects.get(user=request.user)
            return obj.employer == request.user and profile.role == 'employer'
        except UserProfile.DoesNotExist as e:
            return False

