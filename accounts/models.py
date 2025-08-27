from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_dean = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    student_id = models.CharField(max_length=50, null=True, unique=True, blank=True)
    teacher_id = models.CharField(max_length=50, null=True, unique=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='student_profile/images/admin.jpg', blank=True, null=True)

    def __str__(self):
        return self.username
