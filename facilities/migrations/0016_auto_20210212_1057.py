# Generated by Django 2.1.2 on 2021-02-12 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0015_auto_20210212_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityServiceAvailabilityProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Service Availability',
                'verbose_name_plural': '  Service Availability Form',
                'managed': False,
                'proxy': True,
            },
            bases=('facilities.stghealthfacility',),
        ),
        migrations.AddField(
            model_name='facilityserviceavilability',
            name='end_period',
            field=models.IntegerField(default=2021, help_text='This marks the end of reporting. The value must be current             year or greater than the start year', verbose_name='Ending Period'),
        ),
        migrations.AddField(
            model_name='facilityserviceavilability',
            name='period',
            field=models.CharField(blank=True, max_length=25, verbose_name='Period'),
        ),
        migrations.AddField(
            model_name='facilityserviceavilability',
            name='start_period',
            field=models.IntegerField(default=2021, help_text='This marks the start of reporting period', verbose_name='Starting period'),
        ),
        migrations.AlterUniqueTogether(
            name='facilityserviceavilability',
            unique_together={('domain', 'facility')},
        ),
    ]