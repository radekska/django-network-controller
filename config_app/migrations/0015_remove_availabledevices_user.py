# Generated by Django 3.1.1 on 2020-10-01 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config_app', '0014_auto_20201001_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabledevices',
            name='user',
        ),
    ]
