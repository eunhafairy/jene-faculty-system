from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
# Create your models here.

class Research(models.Model):
    class Status(models.TextChoices):
        ONGOING = '1', _("On Going")
        PRESENTED = '2', _("Presented")
        PUBLISHED = '3', _("Published")

    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=9,
        choices=Status.choices,
        default=Status.ONGOING,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="research")
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return self.title