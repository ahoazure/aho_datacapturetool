# Generated by Django 2.2.12 on 2020-11-14 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0014_auto_20201024_0911'),
        ('facilities', '0004_remove_stgfacilityownership_location'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stghealthfacility',
            unique_together={('owner', 'location', 'type', 'name')},
        ),
    ]