from django.urls import path

from core import views

urlpatterns = [
    path(route="", view=views.IndexView.as_view(), name="index",),
    path(
        route="login/",
        view=views.LoginView.as_view(),
        name="login",
    ),
    path(
        route="logout/",
        view=views.LogoutView.as_view(),
        name="logout",
    ),
]
