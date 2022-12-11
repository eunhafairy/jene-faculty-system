from django.contrib import admin

from . import models
# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(models.Subject, SubjectAdmin)