from django.contrib import messages
from django.contrib.auth import views
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic


class IndexView(generic.TemplateView):
    """Homepage view."""

    template_name = "index.html"


class LoginView(SuccessMessageMixin, views.LoginView):
    """Login page view."""

    template_name = "users/login.html"
    next_page: str = reverse_lazy("index")
    success_message: str = _("You are logged in.")


class LogoutView(views.LogoutView):
    """Logout page view."""

    next_page: str = reverse_lazy("index")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        messages.info(request, _("You are logged out."))
        return super().dispatch(request, *args, **kwargs)
