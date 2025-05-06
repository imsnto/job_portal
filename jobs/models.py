from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPost(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    )
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=JOB_TYPES, default='full_time')
    description = models.TextField()
    salary_range = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    employer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
