
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    student_id=models.CharField(max_length=50,null=True,unique=True)
    def __str__(self):
        return self.username

# Create your models here.
