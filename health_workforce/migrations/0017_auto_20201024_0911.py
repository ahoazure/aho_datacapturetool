# Generated by Django 2.1.2 on 2020-10-24 06:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_workforce', '0016_auto_20201002_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stghealthcadretranslation',
            name='shortname',
            field=models.CharField(max_length=230, verbose_name='Short Name'),
        ),
        migrations.AlterField(
            model_name='stgrecurringevent',
            name='external_url',
            field=models.CharField(blank=True, max_length=2083, null=True, verbose_name='Web Address (URL)'),
        ),
        migrations.AlterField(
            model_name='stgrecurringeventtranslation',
            name='shortname',
            field=models.CharField(max_length=230, verbose_name='Short Name'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitutiontranslation',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitutiontranslation',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitutiontranslation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone format: '+999999999' maximum 15.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number'),
        ),
    ]