# Generated by Django 2.1.2 on 2020-07-23 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stgproductdomain',
            options={'managed': True, 'ordering': ('code',), 'verbose_name': 'Resource Category', 'verbose_name_plural': ' Resource Categories'},
        ),
        migrations.AlterModelOptions(
            name='stgproductdomaintranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Resource Category Translation'},
        ),
    ]