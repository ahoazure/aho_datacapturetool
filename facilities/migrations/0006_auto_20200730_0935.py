# Generated by Django 2.1.2 on 2020-07-30 06:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20200730_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stghealthfacilitytranslation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone Number format: '+999999999' maximum 15.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number'),
        ),
    ]