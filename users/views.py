from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from core.mixins import LoginRequiredMixin, ProtectedDeletionMixin
from users.mixins import OnlySelfUserCanEdit
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
    LoginRequiredMixin,
    OnlySelfUserCanEdit,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.User
    template_name = "users/detail.html"
    form_class = forms.UserForm
    success_url = reverse_lazy("users:list")

    author_error_message = "У вас нет прав для изменения другого пользователя."
    author_error_redirect_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно изменен."


class UserDeleteView(
    LoginRequiredMixin,
    OnlySelfUserCanEdit,
    ProtectedDeletionMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    author_error_message = "У вас нет прав для изменения другого пользователя."
    author_error_redirect_url = reverse_lazy("users:list")
    deletion_error_message = (
        "Невозможно удалить пользователя, потому что он используется."
    )

    success_message = "Пользователь успешно удалён."
