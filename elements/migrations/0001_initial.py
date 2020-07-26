# Generated by Django 2.1.2 on 2020-07-23 04:45

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regions', '0002_auto_20200723_0745'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactDataElement',
            fields=[
                ('fact_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=3, max_digits=20, verbose_name='Value')),
                ('target_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Target Value')),
                ('start_year', models.IntegerField(default=2020, verbose_name='Start Year')),
                ('end_year', models.IntegerField(default=2020, verbose_name='Ending Year')),
                ('period', models.CharField(blank=True, max_length=10, verbose_name='Period')),
                ('comment', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Approval Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('categoryoption', models.ForeignKey(default=999, on_delete=django.db.models.deletion.PROTECT, to='home.StgCategoryoption', verbose_name='Disaggregation')),
            ],
            options={
                'verbose_name': 'Data Element',
                'verbose_name_plural': '  Single-Record Form',
                'db_table': 'fact_data_element',
                'ordering': ('location',),
                'permissions': (('approve_factdataelement', 'Can approve Data Element'), ('reject_factdataelement', 'Can reject Data Element'), ('pend_factdataelement', 'Can pend Data Element')),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgDataElement',
            fields=[
                ('dataelement_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=45, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('measuremethod', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgMeasuremethod', verbose_name='Measure Factor')),
            ],
            options={
                'verbose_name': 'Element',
                'verbose_name_plural': 'Data Elements',
                'ordering': ('code',),
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgDataElementGroup',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Group Code')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('dataelement', models.ManyToManyField(blank=True, db_table='stg_data_element_membership', to='elements.StgDataElement')),
            ],
            options={
                'verbose_name': 'Element Group',
                'verbose_name_plural': ' Element Groups',
                'db_table': 'stg_data_element_group',
                'ordering': ('code',),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgDataElementGroupTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=200, verbose_name='Group Name')),
                ('shortname', models.CharField(max_length=120, unique=True, verbose_name='Short Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='elements.StgDataElementGroup')),
            ],
            options={
                'verbose_name': 'Element Group Translation',
                'db_table': 'stg_data_element_group_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgDataElementTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=230)),
                ('shortname', models.CharField(max_length=50, verbose_name='Short name')),
                ('description', models.TextField(blank=True, null=True)),
                ('aggregation_type', models.CharField(choices=[('Sum', 'Sum'), ('Average', 'Average'), ('Count', 'Count'), ('Standard Deviation', 'Standard Deviation'), ('Variance', 'Variance'), ('Min', 'Min'), ('max', 'max'), ('None', 'None')], default='Sum', max_length=45, verbose_name='Data Aggregation')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='elements.StgDataElement')),
            ],
            options={
                'verbose_name': 'Element Translation',
                'db_table': 'elements_stgdataelement_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='dataelement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='elements.StgDataElement', verbose_name='Data Element Name'),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='datasource',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='home.StgDatasource', verbose_name='Data Source'),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='valuetype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgValueDatatype', verbose_name='Data Type'),
        ),
        migrations.CreateModel(
            name='DataElementProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Grid',
                'verbose_name_plural': ' Data Grid',
                'proxy': True,
                'indexes': [],
            },
            bases=('elements.stgdataelement',),
        ),
        migrations.AlterUniqueTogether(
            name='stgdataelementtranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='stgdataelementgrouptranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='factdataelement',
            unique_together={('dataelement', 'location', 'datasource', 'categoryoption', 'start_year', 'end_year')},
        ),
    ]
