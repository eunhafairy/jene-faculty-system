from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
import os
# Create your models here.

#
# admin account : 
# #
# username: admin
# password: django1234
# 

def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    upload_to = 'profile_images/'
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class User(AbstractUser):
    
    class Roles(models.TextChoices):
        ADMIN = '1', _("Admin")
        RSCH_COORD = '2', _("Research Coordinator")
        EXT_COORD = '3', _("Extension Coordinator")
        DEPT_HEAD = '4', _("Department Head")
        FACULTY = '5', _("Faculty")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    is_archived = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=path_and_rename, default='profile_images/default_profile_img.jpg', null=True, blank=True)
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.FACULTY,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
