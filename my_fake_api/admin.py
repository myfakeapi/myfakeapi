from django.contrib import admin

# Register your models here.
from my_fake_api import models

admin.site.register([models.APIHandler, models.APIRequest])