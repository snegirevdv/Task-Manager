from django.contrib import messages
from django.contrib.auth import mixins
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import generic


class OnlyAuthorMixin(generic.detail.SingleObjectMixin, generic.View):
    author_error_message = ""
    redirect = ""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request, self.author_error_message)
            return redirect(self.redirect)
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(mixins.LoginRequiredMixin, generic.View):
    login_error_message = "Вы не авторизованы! Пожалуйста, выполните вход."
    redirect = "login"

    def handle_no_permission(self):
        messages.error(self.request, self.login_error_message)
        return redirect(self.redirect)


class FormMessagesMixin(generic.edit.FormMixin, generic.View):
    form_success_message = ""

    def form_valid(self, form):
        messages.success(self.request, self.form_success_message)
        return super().form_valid(form)
