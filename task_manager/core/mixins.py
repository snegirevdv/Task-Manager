import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import generic

from task_manager.core import consts

logger = logging.getLogger(__name__)


class LoginRequiredMixin(LoginRequiredMixin, generic.View):
    """View requiring login to access the page."""

    def handle_no_permission(self) -> HttpResponse:
        logger.warning("Anonymous user is trying to get a secured page.")

        messages.error(
            self.request,
            consts.Message.FAILURE_NOT_AUTHORIZED.value,
        )
        return redirect("login")


class ProtectedDeletionMixin(generic.DeleteView):
    """Adds a flash message when trying to delete a protected object."""

    deletion_error_message = ""

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)

        except ProtectedError:
            logger.warning(
                f"{request.user} is trying to delete a protected object: "
                f"{self.get_object()}."
            )
            messages.error(request, self.deletion_error_message)
            return redirect(self.success_url)
