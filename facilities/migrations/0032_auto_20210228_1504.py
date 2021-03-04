# Generated by Django 2.1.2 on 2021-02-28 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0031_auto_20210228_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityserviceavailability',
            name='intervention',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='facilities.StgFacilityServiceIntervention', verbose_name='Intervention Areas'),
        ),
        migrations.AlterField(
            model_name='facilityserviceavailability',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='facilities.StgFacilityServiceAreas', verbose_name='Service provision Areas'),
        ),
    ]