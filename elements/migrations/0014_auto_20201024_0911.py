# Generated by Django 2.1.2 on 2020-10-24 06:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0013_auto_20201002_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factdataelement',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
        migrations.AlterField(
            model_name='stgdataelement',
            name='aggregation_type',
            field=models.CharField(choices=[('Count', 'Count'), ('Sum', 'Sum'), ('Average', 'Average'), ('Standard Deviation', 'Standard Deviation'), ('Variance', 'Variance'), ('Min', 'Min'), ('max', 'max'), ('None', 'None')], default='Count', max_length=45, verbose_name='Aggregate Type'),
        ),
        migrations.AlterField(
            model_name='stgdataelement',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Unique ID'),
        ),
    ]