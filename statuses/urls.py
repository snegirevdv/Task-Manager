from django.urls import path

from statuses import views

app_name = "statuses"

urlpatterns = [
    path("create/", views.StatusCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.StatusUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.StatusDeleteView.as_view(), name="delete"),
    path("", views.StatusListView.as_view(), name="list"),
]
