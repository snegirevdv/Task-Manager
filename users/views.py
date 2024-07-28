from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from core import mixins
from users import forms, models


class UserListView(generic.ListView):
    model = models.User
    template_name = "users/list.html"


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    template_name = "users/detail.html"
    form_class = forms.UserForm
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(
    SuccessMessageMixin,
    mixins.LoginRequiredMixin,
    mixins.OnlyAuthorMixin,
    generic.UpdateView,
):
    model = models.User
    template_name = "users/detail.html"
    form_class = forms.UserForm
    success_url = reverse_lazy("users:list")

    author_error_message = "У вас нет прав для изменения другого пользователя."
    redirect = "users:list"
    success_message = "Пользователь успешно изменен."


class UserDeleteView(
    SuccessMessageMixin,
    mixins.LoginRequiredMixin,
    mixins.OnlyAuthorMixin,
    generic.DeleteView,
):
    model = models.User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    author_error_message = "У вас нет прав для изменения другого пользователя."
    redirect = "users:list"
    success_message = "Пользователь успешно удалён."
