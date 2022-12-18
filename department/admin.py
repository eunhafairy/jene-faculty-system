from django.contrib import admin

from . import models
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code",)

admin.site.register(models.Department, DepartmentAdmin)