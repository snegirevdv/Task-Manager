from django.contrib import messages
from django.contrib.auth import views
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views import generic

from task_manager.core import consts


class IndexView(generic.TemplateView):
    """Homepage view."""

    template_name: str = consts.Template.INDEX.value


class LoginView(SuccessMessageMixin, views.LoginView):
    """Login page view."""

    template_name: str = consts.Template.LOGIN.value
    success_message: str = consts.Message.SUCCESS_LOGIN.value
    next_page: str = reverse_lazy("index")


class LogoutView(views.LogoutView):
    """Logout page view."""

    next_page: str = reverse_lazy("index")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        messages.info(request, consts.Message.SUCCESS_LOGOUT.value)
        return super().dispatch(request, *args, **kwargs)
