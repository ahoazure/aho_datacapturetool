# Generated by Django 2.1.2 on 2020-08-10 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0010_auto_20200810_1940'),
        ('home', '0012_auto_20200731_1246'),
        ('indicators', '0012_auto_20200731_1328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aho_factsindicator_archive',
            options={'managed': False, 'ordering': ('indicator__name', 'location__name'), 'verbose_name': 'Archive', 'verbose_name_plural': 'Indicators Archive'},
        ),
        migrations.AlterModelOptions(
            name='ahodoamain_lookup',
            options={'managed': False, 'ordering': ('indicator_name',), 'verbose_name': 'Theme Lookup', 'verbose_name_plural': 'Themes Lookup'},
        ),
        migrations.AlterModelOptions(
            name='factdataindicator',
            options={'managed': True, 'ordering': ('indicator__name', 'location__name'), 'permissions': (('approve_factdataindicator', 'Can approve Indicator Data'), ('reject_factdataindicator', 'Can reject Indicator Data'), ('pend_factdataindicator', 'Can pend Indicator Data')), 'verbose_name': 'Indicator Record', 'verbose_name_plural': 'Single-Record Form'},
        ),
        migrations.AlterModelOptions(
            name='stgindicator',
            options={'managed': True, 'verbose_name': 'Indicator', 'verbose_name_plural': 'Indicators'},
        ),
        migrations.AlterModelOptions(
            name='stgindicatordomain',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Indicator Theme', 'verbose_name_plural': 'Indicator Themes'},
        ),
        migrations.AlterModelOptions(
            name='stgindicatornarrative',
            options={'managed': True, 'ordering': ('-narrative_type',), 'verbose_name': 'Indicator Narrative', 'verbose_name_plural': 'Indicators Narrative'},
        ),
        migrations.AlterModelOptions(
            name='stgindicatorreference',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Indicator Reference', 'verbose_name_plural': 'Indicator References'},
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='categoryoption',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.PROTECT, to='home.StgCategoryoption', verbose_name='Disaggregation Options'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='comment',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='denominator_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Denominator Value'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='end_period',
            field=models.IntegerField(default=2020, help_text='This marks the end of reporting. The value must be current             year or greater than the start year', verbose_name='Ending Period'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='measuremethod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.StgMeasuremethod', verbose_name='Measure Type'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='numerator_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Numerator Value'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='start_period',
            field=models.IntegerField(default=2020, help_text='This marks the start of reporting period', verbose_name='Starting period'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='string_value',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='factdataindicator',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='narrative_text',
            field=models.TextField(verbose_name='Narrative Text'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='narrative_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicators.StgNarrative_Type', verbose_name='Narrative Type'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgindicator',
            name='afrocode',
            field=models.CharField(blank=True, max_length=10, unique=True, verbose_name='Regional Code'),
        ),
        migrations.AlterField(
            model_name='stgindicator',
            name='gen_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Global Code'),
        ),
        migrations.AlterField(
            model_name='stgindicator',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgindicatordomain',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorDomain', verbose_name='Parent Theme'),
        ),
        migrations.AlterField(
            model_name='stgindicatordomain',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgindicatordomaintranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stgindicatordomaintranslation',
            name='level',
            field=models.SmallIntegerField(default=1, verbose_name='Theme Level'),
        ),
        migrations.AlterField(
            model_name='stgindicatordomaintranslation',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Theme'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='narrative_text',
            field=models.TextField(verbose_name='Narrative Text'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='narrative_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicators.StgNarrative_Type', verbose_name='Narratice Type'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgindicatorreference',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='unique ID'),
        ),
        migrations.AlterField(
            model_name='stgindicatorreferencetranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stgindicatortranslation',
            name='preferred_datasources',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Primary Sources'),
        ),
        migrations.AlterField(
            model_name='stgnarrative_type',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgnarrative_typetranslation',
            name='description',
            field=models.TextField(null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterUniqueTogether(
            name='factdataindicator',
            unique_together={('indicator', 'location', 'categoryoption', 'datasource', 'start_period', 'end_period')},
        ),
    ]
