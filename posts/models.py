from django.db import models
from accounts.models import User
# Create your models here.

class Post(models.Model):
    class PostType(models.TextChoices):
        NEWS = "1", "News"
        EVENT = "2", "Event"
        RSCH = "3", "Research-related"
        EXT = "4", "Extension-related"



    title = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(max_length=9,
                            choices=PostType.choices,
                            default=PostType.NEWS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created = models.DateTimeField(auto_now_add=True)