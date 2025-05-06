from rest_framework import permissions

from users.models import UserProfile

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        try:
            profile = UserProfile.objects.get(user=request.user)
            return request.user.is_authenticated and profile.role == 'employer'
        except Exception as e:
            return False

