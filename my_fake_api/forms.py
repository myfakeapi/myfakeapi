from my_fake_api import models
from django import forms


class HandlerCreateForm(forms.ModelForm):

    class Meta:
        model = models.APIHandler
        exclude = ["user"]
