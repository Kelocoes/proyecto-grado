# Generated by Django 4.2.1 on 2023-05-30 04:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AppBack", "0004_rename_results_medic_matient_results_medic_patient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="patient_id",
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
