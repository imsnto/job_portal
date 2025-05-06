from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class UserProfile(models.Model):
    USER_ROLES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='job_seeker')


