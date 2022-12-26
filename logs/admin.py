from django.contrib import admin

from . import models
# Register your models here.
class LogAdmin(admin.ModelAdmin):
    list_display = ("log_message",)

admin.site.register(models.Log, LogAdmin)