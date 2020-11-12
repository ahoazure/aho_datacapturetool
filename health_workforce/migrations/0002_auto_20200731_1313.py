# Generated by Django 2.1.2 on 2020-07-31 10:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20200731_1246'),
        ('regions', '0009_auto_20200727_2255'),
        ('publications', '0007_stgresourcetypetranslation_categorization'),
        ('health_workforce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StgHealthCadre',
            fields=[
                ('cadre_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique Universal ID')),
                ('code', models.CharField(blank=True, max_length=45, unique=True, verbose_name='ISCO-08 Code')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
            ],
            options={
                'verbose_name': 'Health Occupation',
                'verbose_name_plural': ' Health Occupations',
                'db_table': 'stg_health_cadre',
                'ordering': ('code',),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgHealthCadreTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=230, verbose_name='Cadre/occupation Name')),
                ('shortname', models.CharField(default='Not Available', max_length=230, verbose_name='Short Name')),
                ('academic', models.CharField(blank=True, max_length=500, null=True, verbose_name='Qualification Level')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='health_workforce.StgHealthCadre')),
            ],
            options={
                'verbose_name': 'Health Occupation Translation',
                'db_table': 'stg_health_cadre_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgHealthWorkforceFacts',
            fields=[
                ('fact_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique Universal ID')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=20, verbose_name='Data Value')),
                ('start_year', models.IntegerField(default=2020, verbose_name='Start Year')),
                ('end_year', models.IntegerField(default=2020, verbose_name='Ending Year')),
                ('period', models.CharField(blank=True, max_length=10, verbose_name='Period')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('cadre_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='health_workforce.StgHealthCadre', verbose_name='Occupation/Cadre')),
                ('categoryoption', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgCategoryoption', verbose_name='Disaggregation')),
                ('datasource', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgDatasource', verbose_name='Data Source')),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Geographical Location')),
                ('measuremethod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.StgMeasuremethod', verbose_name='Type of Measure')),
            ],
            options={
                'verbose_name': 'Healthworkforce Data',
                'verbose_name_plural': '  Healthworkforce Data',
                'db_table': 'fact_health_workforce',
                'ordering': ('cadre_id',),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgInstitutionType',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique Universal ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Code')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
            ],
            options={
                'verbose_name': 'Institution Type',
                'verbose_name_plural': 'Institution Types',
                'db_table': 'stg_institution_type',
                'ordering': ('code',),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgInstitutionTypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=230, verbose_name='Resource Type Name')),
                ('shortname', models.CharField(blank=True, max_length=230, null=True, verbose_name='Short Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='health_workforce.StgInstitutionType')),
            ],
            options={
                'verbose_name': 'Institution Type Translation',
                'db_table': 'stg_institution_type_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgTrainingInstitution',
            fields=[
                ('institution_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique Universal ID')),
                ('code', models.CharField(blank=True, max_length=15, unique=True, verbose_name='Institution Code')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('location', models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Geographical Location')),
                ('type', models.ForeignKey(default=6, on_delete=django.db.models.deletion.PROTECT, to='health_workforce.StgInstitutionType', verbose_name='Institution Type')),
            ],
            options={
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Training Institutions',
                'db_table': 'stg_traininginstitution',
                'ordering': ['code'],
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgTrainingInstitutionTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=230, verbose_name='Institution Name')),
                ('programmes', models.TextField(blank=True, null=True, verbose_name='Training Programs')),
                ('faculty', models.CharField(blank=True, max_length=150, null=True, verbose_name='Faculty Name')),
                ('accreditation', models.CharField(choices=[('accredited', 'Accredited'), ('charterted', 'Chartered'), ('unacredited', 'Not Accredited'), ('pending', 'Pending Accreditation')], default='accredited', max_length=50, verbose_name='Accreditation Status')),
                ('regulator', models.CharField(blank=True, max_length=150, null=True, verbose_name='Regulatory Body')),
                ('accreditation_info', models.CharField(blank=True, max_length=2000, verbose_name='Accreditation Details')),
                ('language', models.CharField(max_length=50, verbose_name='Teaching Language')),
                ('address', models.CharField(max_length=500, verbose_name='Contact Address/Person')),
                ('posta', models.CharField(blank=True, max_length=500, verbose_name='Postal Address')),
                ('email', models.EmailField(blank=True, max_length=250, unique=True, verbose_name='Email Address')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone Number format: '+999999999' maximum 15.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number')),
                ('url', models.URLField(blank=True, max_length=2083, null=True, verbose_name='Web Address')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='health_workforce.StgTrainingInstitution')),
            ],
            options={
                'verbose_name': 'Institution Translation',
                'db_table': 'stg_traininginstitution_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HumanWorkforceResourceProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Resource & Guide',
                'verbose_name_plural': ' Resources & Guides',
                'proxy': True,
                'indexes': [],
            },
            bases=('publications.stgknowledgeproduct',),
        ),
        migrations.AlterModelOptions(
            name='resourcetypeproxy',
            options={'verbose_name': 'Resource Type', 'verbose_name_plural': ' Resource Types'},
        ),
        migrations.AlterUniqueTogether(
            name='stgtraininginstitutiontranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='stginstitutiontypetranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='stghealthcadretranslation',
            unique_together={('language_code', 'master')},
        ),
    ]