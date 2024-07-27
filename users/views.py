from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from users import forms, models


class OnlyAuthorMixin:
    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return redirect("users:list")
        return super().get(request, *args, **kwargs)


class UserListView(generic.ListView):
    model = models.User
    template_name = "users/list.html"


class UserCreateView(generic.CreateView):
    template_name = "users/detail.html"
    form_class = forms.UserForm
    success_url = reverse_lazy("login")


class UserUpdateView(OnlyAuthorMixin, generic.UpdateView):
    model = models.User
    template_name = "users/detail.html"
    form_class = forms.UserForm
    success_url = reverse_lazy("users:list")


class UserDeleteView(OnlyAuthorMixin, generic.DeleteView):
    model = models.User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
