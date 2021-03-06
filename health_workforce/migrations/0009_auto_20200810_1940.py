# Generated by Django 2.1.2 on 2020-08-10 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('health_workforce', '0008_auto_20200731_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='humanworkforceresourceproxy',
            options={'verbose_name': 'Resource/Guide', 'verbose_name_plural': 'Resources/Guides'},
        ),
        migrations.AlterModelOptions(
            name='resourcetypeproxy',
            options={'verbose_name': 'Resource Type', 'verbose_name_plural': 'Resource Types'},
        ),
        migrations.AlterModelOptions(
            name='stghealthcadre',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Health Cadre', 'verbose_name_plural': 'Health Cadres'},
        ),
        migrations.AlterModelOptions(
            name='stghealthworkforcefacts',
            options={'managed': True, 'ordering': ('cadre_id',), 'verbose_name': 'Healthworkforce Data', 'verbose_name_plural': 'Healthworkforce Data'},
        ),
        migrations.AlterModelOptions(
            name='stginstitutionprogrammes',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Training Programme', 'verbose_name_plural': 'Training Programmes'},
        ),
        migrations.AlterModelOptions(
            name='stginstitutionprogrammestranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Training Programme Translation'},
        ),
        migrations.AlterField(
            model_name='stghealthcadre',
            name='parent',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='health_workforce.StgHealthCadre', verbose_name='Parent Cadre'),
        ),
        migrations.AlterField(
            model_name='stghealthcadre',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stghealthcadretranslation',
            name='academic',
            field=models.CharField(choices=[('degree', 'Degree'), ('diploma', 'Diploma'), ('masters', 'Masters'), ('phd', 'Doctorate'), ('certificate', 'Certificate'), ('basic', 'Basic Education')], default='degree', max_length=10, verbose_name='Academic Qualification'),
        ),
        migrations.AlterField(
            model_name='stghealthcadretranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stghealthworkforcefacts',
            name='end_year',
            field=models.IntegerField(default=2020, verbose_name='Ending Period'),
        ),
        migrations.AlterField(
            model_name='stghealthworkforcefacts',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='stghealthworkforcefacts',
            name='measuremethod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.StgMeasuremethod', verbose_name='Measure Type'),
        ),
        migrations.AlterField(
            model_name='stghealthworkforcefacts',
            name='start_year',
            field=models.IntegerField(default=2020, verbose_name='Starting Period'),
        ),
        migrations.AlterField(
            model_name='stghealthworkforcefacts',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stginstitutionprogrammes',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stginstitutionprogrammestranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stginstitutionprogrammestranslation',
            name='name',
            field=models.CharField(max_length=230, verbose_name='Type Name'),
        ),
        migrations.AlterField(
            model_name='stginstitutiontype',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stginstitutiontypetranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stginstitutiontypetranslation',
            name='name',
            field=models.CharField(max_length=230, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitution',
            name='location',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitution',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitutiontranslation',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Contact Person'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitutiontranslation',
            name='email',
            field=models.EmailField(blank=True, max_length=250, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='stgtraininginstitutiontranslation',
            name='posta',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Post Address'),
        ),
    ]
