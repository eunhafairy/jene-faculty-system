from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from accounts.models import User

class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="department", null=True)
    def __str__(self):
      return self.name