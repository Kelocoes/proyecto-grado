# Generated by Django 4.2.1 on 2023-06-13 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppBack', '0002_user_is_disabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_disabled',
        ),
    ]
