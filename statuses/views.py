from django.urls import reverse_lazy
from django.views import generic

from statuses import forms, models


class StatusListView(generic.ListView):
    model = models.Status
    template_name = "statuses/list.html"


class StatusCreateView(generic.CreateView):
    model = models.Status
    form_class = forms.StatusForm
    template_name = "statuses/detail.html"
    success_url = reverse_lazy("statuses:list")


class StatusUpdateView(generic.UpdateView):
    model = models.Status
    form_class = forms.StatusForm
    template_name = "statuses/detail.html"
    success_url = reverse_lazy("statuses:list")


class StatusDeleteView(generic.DeleteView):
    model = models.Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
