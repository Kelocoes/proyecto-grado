# Generated by Django 4.2.1 on 2023-06-13 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppBack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
    ]
