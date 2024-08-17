# Generated by Django 5.0.7 on 2024-08-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="taskstatus",
            options={
                "verbose_name": "статус",
                "verbose_name_plural": "Statuses",
            },
        ),
        migrations.AlterField(
            model_name="taskstatus",
            name="name",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Name"
            ),
        ),
    ]
