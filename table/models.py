from django.db import models
from accounts.models import User
from subjects.models import Subject
from extensions.models import Extension
# Create your models here.

class FacultySubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject")
    created = models.DateTimeField(auto_now_add=True)

   
class FacultyExtension(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    ext = models.ForeignKey(Extension, on_delete=models.CASCADE, related_name="ext")
    created = models.DateTimeField(auto_now_add=True)

   