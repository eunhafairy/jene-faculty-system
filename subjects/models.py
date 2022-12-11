from django.db import models
from accounts.models import User
# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=55, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subjects")
    created = models.DateTimeField(auto_now_add=True)