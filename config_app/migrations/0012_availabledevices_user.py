# Generated by Django 3.1.1 on 2020-10-01 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('config_app', '0011_auto_20201001_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabledevices',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
