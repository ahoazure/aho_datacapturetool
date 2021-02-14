# Generated by Django 2.1.2 on 2021-02-14 12:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0019_auto_20210214_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='stghealthfacility',
            name='phone_code',
            field=models.CharField(choices=[(242, 242), (244, 244), (254, 254), (256, 256), (263, 263)], default=242, max_length=50, verbose_name='Country Code'),
        ),
        migrations.AddField(
            model_name='stghealthfacility',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone format: '+999999999' maximum 15.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Telephone'),
        ),
        migrations.AddField(
            model_name='stghealthfacility',
            name='phone_part',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone format: '+999999999' maximum 15.", regex='^[0-9]+{9,15}$')], verbose_name='Phone Number'),
        ),
    ]
