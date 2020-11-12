# Generated by Django 2.1.2 on 2020-08-10 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0009_auto_20200727_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stglocation',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Location', 'verbose_name_plural': 'Locations'},
        ),
        migrations.AlterModelOptions(
            name='stgspecialcategorization',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Categorization', 'verbose_name_plural': 'Special Categorizations'},
        ),
        migrations.AlterModelOptions(
            name='stgspecialcategorizationtranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Categorization Translation'},
        ),
        migrations.AlterField(
            model_name='stgeconomiczones',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgeconomiczonestranslation',
            name='name',
            field=models.CharField(max_length=230, verbose_name='Economic Zone'),
        ),
        migrations.AlterField(
            model_name='stglocation',
            name='code',
            field=models.CharField(blank=True, max_length=15, unique=True, verbose_name='Unique Code'),
        ),
        migrations.AlterField(
            model_name='stglocation',
            name='parent',
            field=models.ForeignKey(blank=True, default=1, help_text='You are not allowed to edit this field because it is         related to other records', null=True, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Parent Location'),
        ),
        migrations.AlterField(
            model_name='stglocation',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stglocation',
            name='wb_income',
            field=models.ForeignKey(default='99', on_delete=django.db.models.deletion.PROTECT, to='regions.StgWorldbankIncomegroups', verbose_name='Income level'),
        ),
        migrations.AlterField(
            model_name='stglocation',
            name='zone',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.PROTECT, to='regions.StgEconomicZones', verbose_name='Economic Zone'),
        ),
        migrations.AlterField(
            model_name='stglocationlevel',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stglocationleveltranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stglocationleveltranslation',
            name='type',
            field=models.CharField(choices=[('level 1', 'level 1'), ('Level 2', 'Level 2'), ('Level 3', 'Level 3'), ('Level 4', 'Level 4'), ('Level 5', 'Level 5'), ('Level 6', 'Level 6'), ('Level 7', 'Level 7')], default='level 1', max_length=50, verbose_name='Location Level'),
        ),
        migrations.AlterField(
            model_name='stglocationtranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stgspecialcategorization',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgspecialcategorizationtranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stgspecialcategorizationtranslation',
            name='name',
            field=models.CharField(max_length=230, verbose_name='Categorization Name'),
        ),
        migrations.AlterField(
            model_name='stgworldbankincomegroups',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgworldbankincomegroupstranslation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='stgworldbankincomegroupstranslation',
            name='name',
            field=models.CharField(max_length=230, verbose_name='Income level'),
        ),
    ]
