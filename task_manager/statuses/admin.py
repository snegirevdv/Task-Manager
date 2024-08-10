from django.contrib import admin

from task_manager.statuses import models

admin.site.register(models.TaskStatus)
