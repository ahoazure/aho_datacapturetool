# Generated by Django 2.1.2 on 2021-03-04 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0050_auto_20210304_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityserviceavailability',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Name (Email)'),
        ),
    ]
