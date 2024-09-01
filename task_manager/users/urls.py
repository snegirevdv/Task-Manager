from django.urls import path

from task_manager.users import views

app_name = "users"

urlpatterns = [
    path(
        route="create/",
        view=views.UserCreateView.as_view(),
        name="create",
    ),
    path(
        route="<int:pk>/update/",
        view=views.UserUpdateView.as_view(),
        name="update",
    ),
    path(
        route="<int:pk>/delete/",
        view=views.UserDeleteView.as_view(),
        name="delete",
    ),
]
