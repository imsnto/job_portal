from django.db import models
from django.contrib.auth import get_user_model

from jobs.models import JobPost

User = get_user_model()

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('shortlisted', 'Shortlisted')
    )
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('applicant', 'job_post')

    def __str__(self):
        return f'{self.applicant} applied for {self.job_post}'

