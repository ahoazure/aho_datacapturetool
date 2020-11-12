# Generated by Django 2.1.2 on 2020-07-27 09:39

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_auto_20200727_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='StgNarrative_TypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=500, verbose_name='Name')),
                ('shortname', models.CharField(max_length=120, null=True, unique=True, verbose_name='Short Name')),
                ('description', models.TextField(null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Narrative Type Translation',
                'db_table': 'stg_narrative_type_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.AlterModelOptions(
            name='stganalyticsnarrative',
            options={'managed': True, 'ordering': ('-narrative_type',), 'verbose_name': 'Theme Narrative', 'verbose_name_plural': 'Theme Narratives'},
        ),
        migrations.AlterModelOptions(
            name='stgnarrative_type',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Narrative Type', 'verbose_name_plural': 'Narrative Types'},
        ),
        migrations.RemoveField(
            model_name='stgnarrative_type',
            name='description',
        ),
        migrations.RemoveField(
            model_name='stgnarrative_type',
            name='name',
        ),
        migrations.RemoveField(
            model_name='stgnarrative_type',
            name='shortname',
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='code',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorDomain', verbose_name='Theme'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='narrative_text',
            field=models.TextField(verbose_name=' Narrative'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='narrative_type',
            field=models.ForeignKey(db_column='narrative_type_id', on_delete=django.db.models.deletion.PROTECT, to='indicators.StgNarrative_Type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='code',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicator', verbose_name='Indicator'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='narrative_text',
            field=models.TextField(verbose_name=' Narrative'),
        ),
        migrations.AlterField(
            model_name='stgindicatornarrative',
            name='narrative_type',
            field=models.ForeignKey(db_column='narrative_type_id', on_delete=django.db.models.deletion.PROTECT, to='indicators.StgNarrative_Type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='stgnarrative_type',
            name='code',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Code'),
        ),
        migrations.AddField(
            model_name='stgnarrative_typetranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='indicators.StgNarrative_Type'),
        ),
        migrations.AlterUniqueTogether(
            name='stgnarrative_typetranslation',
            unique_together={('language_code', 'master')},
        ),
    ]