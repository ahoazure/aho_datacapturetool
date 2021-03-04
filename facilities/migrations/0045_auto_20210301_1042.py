# Generated by Django 2.1.2 on 2021-03-01 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0044_auto_20210301_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='stghealthfacility',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Name (Email)'),
        ),
        migrations.AlterField(
            model_name='stghealthfacility',
            name='location',
            field=models.ForeignKey(default=24, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Facility Country'),
        ),
    ]