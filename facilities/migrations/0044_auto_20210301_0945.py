# Generated by Django 2.1.2 on 2021-03-01 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0043_auto_20210301_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgfacilitylocation',
            name='country_code',
            field=models.CharField(max_length=15, unique=True, verbose_name='Phone Code'),
        ),
        migrations.AlterField(
            model_name='stghealthfacility',
            name='country_code',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='facilities.StgFacilityLocation', verbose_name='Country Phone Code '),
        ),
        migrations.AlterField(
            model_name='stghealthfacility',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Facility Country'),
        ),
    ]