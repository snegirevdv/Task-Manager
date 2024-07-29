from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.utils.translation import gettext_lazy as _

from core.mixins import LoginRequiredMixin, ProtectedDeletionMixin
from users.mixins import OnlySelfUserCanEdit
from users import forms, models


class UserListView(generic.ListView):
    """User list view."""
    model = models.User
    template_name = "users/list.html"


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    """User registration view."""

    template_name = "users/create_update.html"
    form_class = forms.UserForm
    success_url: str = reverse_lazy("login")
    success_message: str = _("The user has been successfully registered.")


class UserUpdateView(
    LoginRequiredMixin,
    OnlySelfUserCanEdit,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """User editing view."""

    model = models.User
    template_name = "users/create_update.html"
    form_class = forms.UserForm
    success_url: str = reverse_lazy("users:list")
    success_message = _("The user has been successfully updated.")


class UserDeleteView(
    LoginRequiredMixin,
    OnlySelfUserCanEdit,
    ProtectedDeletionMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """User deletion view."""

    model = models.User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    deletion_error_message = (
        _("The user cannot be deleted because it is in use.")
    )

    success_message = _("The user has been successfully deleted.")
