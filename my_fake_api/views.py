from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from my_fake_api import models
from my_fake_api import forms


class HandlerCreate(CreateView):

    success_url = reverse_lazy("my_fake_api:handler_list")
    form_class = forms.HandlerCreateForm
    template_name = "my_fake_api/handler_create.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class HandlerList(ListView):

    model = models.APIHandler
    template_name = "my_fake_api/handler_list.html"


class HandlerDetails(DetailView):
    model = models.APIHandler
    template_name = "my_fake_api/handler_details.html"


class HandlerLogs(DetailView):
    model = models.APIHandler
    template_name = "my_fake_api/handler_logs.html"
