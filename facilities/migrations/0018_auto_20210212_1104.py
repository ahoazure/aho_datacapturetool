# Generated by Django 2.1.2 on 2021-02-12 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0017_auto_20210212_1101'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='facilityserviceavilability',
            unique_together={('domain', 'facility', 'start_period', 'end_period', 'intervention')},
        ),
    ]
