# Generated by Django 2.2.12 on 2021-02-02 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0014_auto_20201024_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factdataelement',
            name='end_year',
            field=models.IntegerField(default=2021, verbose_name='Ending Year'),
        ),
        migrations.AlterField(
            model_name='factdataelement',
            name='start_year',
            field=models.IntegerField(default=2021, verbose_name='Start Year'),
        ),
    ]
