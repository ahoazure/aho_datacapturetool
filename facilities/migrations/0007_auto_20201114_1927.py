# Generated by Django 2.2.12 on 2020-11-14 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0014_auto_20201024_0911'),
        ('facilities', '0006_auto_20201114_1925'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stghealthfacility',
            unique_together={('owner', 'location', 'type')},
        ),
    ]