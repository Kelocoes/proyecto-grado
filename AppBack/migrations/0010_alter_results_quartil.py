# Generated by Django 4.2.1 on 2023-07-29 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AppBack", "0009_results_framingham"),
    ]

    operations = [
        migrations.AlterField(
            model_name="results",
            name="quartil",
            field=models.CharField(default="1", max_length=10),
        ),
    ]
