# Generated by Django 2.1.2 on 2021-02-11 20:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0012_remove_stgservicedomain_facilities'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityServiceAvilability',
            fields=[
                ('availability_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID')),
                ('code', models.CharField(blank=True, max_length=45, unique=True)),
                ('intervention', models.CharField(choices=[('NCD health promotion', 'NCD promotion'), ('CD health promotion', 'Child health promotion'), ('Child health promotion', 'Child health promotion'), ('Adolescent health promotion', 'Adolescent health promotion'), ('Adult health promotion', 'Adult health promotion'), ('Elderly health promotion', 'Elderly health promotion')], default='NCD health promotion', max_length=50, verbose_name='Intervention area')),
                ('service', models.CharField(choices=[('NCD HPR', 'NCD HPR'), ('CD health HPR', 'Child health HPR'), ('Child health HPR', 'Child health HPR'), ('Adolescent health HPR ', 'Adolescent health HPR'), ('Adult health HPR', 'Adult health HPR'), ('Elderly health HPR', 'Elderly health HPR')], default='NCD HPR', max_length=50, verbose_name='Service provision area)')),
                ('provided', models.BooleanField(default=False, verbose_name='Service Provided last 3 Months?')),
                ('specialunit', models.BooleanField(default=False, verbose_name='Specialized Unit Provided?')),
                ('staff', models.BooleanField(default=False, verbose_name='Staff Capacity Appropriate?')),
                ('infrastructure', models.BooleanField(default=False, verbose_name='Infrastructure Capacity Appropriate?')),
                ('supplies', models.BooleanField(default=False, verbose_name='Supplies Appropriate?')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.StgServiceDomain', verbose_name='Service Domain')),
            ],
            options={
                'verbose_name': 'Service Availability',
                'verbose_name_plural': 'Services Avilability',
                'db_table': 'stg_facility_services_availability',
                'ordering': ('domain',),
                'managed': True,
            },
        ),
    ]
