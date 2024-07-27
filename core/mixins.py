from django.contrib import messages
from django.contrib.auth import mixins
from django.shortcuts import redirect
from django.views import generic


class OnlyAuthorMixin(
    mixins.UserPassesTestMixin,
    generic.detail.SingleObjectMixin,
    generic.View,
):
    author_error_message = ""
    redirect_url = ""

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, self.author_error_message)
        return redirect(self.redirect_url)


class LoginRequiredMixin(mixins.LoginRequiredMixin, generic.View):
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход.",
        )
        return redirect("login")
