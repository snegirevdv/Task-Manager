from django.contrib import admin

from task_manager.labels import models

admin.site.register(models.TaskLabel)
