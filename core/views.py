from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "index.html"


class LoginView(views.LoginView):
    template_name = "users/login.html"
    next_page = reverse_lazy("index")


class LogoutView(views.LogoutView):
    next_page = reverse_lazy("index")
