from django.contrib import admin

from task_manager.tasks import models

admin.site.register(models.Task)
