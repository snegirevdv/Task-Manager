from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("labels/", include("labels.urls")),
    path("tasks/", include("tasks.urls")),
    path("", include("core.urls")),
    path('i18n/', include('django.conf.urls.i18n')),

]
