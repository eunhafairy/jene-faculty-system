from django.contrib import admin

from . import models
# Register your models here.
class ResearchAdmin(admin.ModelAdmin):
    list_display = ("title",)

admin.site.register(models.Research, ResearchAdmin)