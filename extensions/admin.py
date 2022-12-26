from django.contrib import admin

from . import models
# Register your models here.
class ExtensionAdmin(admin.ModelAdmin):
    list_display = ("code",)

admin.site.register(models.Extension, ExtensionAdmin)