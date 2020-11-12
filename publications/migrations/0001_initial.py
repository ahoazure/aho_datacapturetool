# Generated by Django 2.1.2 on 2020-07-23 04:59

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regions', '0002_auto_20200723_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='StgKnowledgeProduct',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('internal_url', models.FileField(blank=True, upload_to='media/files', verbose_name='File')),
                ('external_url', models.CharField(blank=True, max_length=2083, null=True)),
                ('cover_image', models.ImageField(blank=True, upload_to='media/images', verbose_name='Image')),
                ('comment', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Status')),
                ('code', models.CharField(blank=True, max_length=45, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Publisher Location')),
            ],
            options={
                'verbose_name': 'Knowledge Resource',
                'verbose_name_plural': '  Knowledge Resources',
                'db_table': 'stg_knowledge_product',
                'ordering': ('code',),
                'permissions': (('approve_stgknowledgeproduct', 'Can approve stgknowledgeproduct'), ('reject_stgknowledgeproduct', 'Can reject stgknowledgeproduct'), ('pend_stgknowledgeproduct', 'Can pend stgknowledgeproduct')),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgKnowledgeProductTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=230, verbose_name='Title')),
                ('categorization', models.CharField(choices=[('toolkit', 'Toolkit'), ('publication', 'Publication')], default='toolkit', help_text='You must specify the published resource as a scienctific             publication or a toolkit.Toolkit are resources like  M&E Guides ', max_length=15, verbose_name='Categorization')),
                ('description', models.TextField(blank=True, null=True)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('author', models.CharField(max_length=200, verbose_name='Author/Owner')),
                ('year_published', models.IntegerField(default=2020, verbose_name='Year Published')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='publications.StgKnowledgeProduct')),
            ],
            options={
                'verbose_name': 'Knowledge Resource Translation',
                'db_table': 'stg_knowledge_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgProductDomain',
            fields=[
                ('domain_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Domain Code')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publications.StgProductDomain', verbose_name='Parent Domain')),
                ('publications', models.ManyToManyField(blank=True, db_table='stg_product_domain_members', to='publications.StgKnowledgeProduct', verbose_name='Publications')),
            ],
            options={
                'verbose_name': 'Publication Category',
                'verbose_name_plural': ' Knowledge Categories',
                'db_table': 'stg_publication_domain',
                'ordering': ('code',),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgProductDomainTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=230, verbose_name='Domain Name')),
                ('shortname', models.CharField(max_length=45, null=True, verbose_name='Short Name')),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(default=1, verbose_name='Level')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='publications.StgProductDomain')),
            ],
            options={
                'verbose_name': 'Publication Category Translation',
                'db_table': 'stg_publication_domain_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgResourceType',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Code')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Resource Types',
                'db_table': 'stg_resource_type',
                'ordering': ('code',),
                'managed': True,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StgResourceTypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=230, verbose_name='Resource Type Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='publications.StgResourceType')),
            ],
            options={
                'verbose_name': 'Type Translation',
                'db_table': 'stg_resource_type_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='stgknowledgeproduct',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications.StgResourceType', verbose_name='Resource Type'),
        ),
        migrations.AlterUniqueTogether(
            name='stgresourcetypetranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='stgproductdomaintranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='stgknowledgeproducttranslation',
            unique_together={('language_code', 'master')},
        ),
    ]