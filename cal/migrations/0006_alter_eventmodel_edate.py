# Generated by Django 5.0.2 on 2024-02-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cal", "0005_alter_eventmodel_edate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventmodel",
            name="edate",
            field=models.DateField(max_length=100),
        ),
    ]
