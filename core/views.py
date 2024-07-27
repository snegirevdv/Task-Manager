from django.contrib import messages
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "index.html"


class LoginView(views.LoginView):
    template_name = "users/login.html"
    next_page = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_invalid(form)


class LogoutView(views.LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
