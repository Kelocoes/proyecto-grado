# Generated by Django 4.2.1 on 2023-07-29 19:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("AppBack", "0010_alter_results_quartil"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patient",
            name="creation_date",
        ),
    ]
