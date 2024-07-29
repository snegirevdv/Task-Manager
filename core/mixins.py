from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic


class LoginRequiredMixin(LoginRequiredMixin, generic.View):
    """View requiring login to access the page."""

    def handle_no_permission(self) -> HttpResponse:
        messages.error(
            self.request,
            _("You are not authorized! Please log in again."),
        )
        return redirect("login")


class ProtectedDeletionMixin(generic.DeleteView):
    """Adds a flash message when trying to delete a protected object."""

    deletion_error_message = ""

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)

        except ProtectedError:
            messages.error(request, self.deletion_error_message)
            return redirect(self.success_url)
