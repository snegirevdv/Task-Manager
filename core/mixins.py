from django.contrib import messages
from django.contrib.auth import mixins
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views import generic


class LoginRequiredMixin(mixins.LoginRequiredMixin, generic.View):
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход.",
        )
        return redirect("login")


class ProtectedDeletionMixin(generic.DeleteView):
    deletion_error_message = ""

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.deletion_error_message)
            return redirect(self.success_url)
