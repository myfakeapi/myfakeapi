"""
Application admin configuration
"""
from django.contrib import admin

from my_fake_api import models


class APIRequestInlines(admin.TabularInline):
    model = models.APIRequest


class APIHandlerAdmin(admin.ModelAdmin):
    inlines = (APIRequestInlines, )


admin.site.register(models.APIHandler, APIHandlerAdmin)
