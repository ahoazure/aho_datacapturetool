# Generated by Django 2.1.2 on 2020-08-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0014_auto_20200810_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgindicatordomain',
            name='level',
            field=models.CharField(choices=[('level 1', 'level 1'), ('Level 2', 'Level 2'), ('Level 3', 'Level 3'), ('Level 4', 'Level 4'), ('Level 5', 'Level 5')], default='level 1', max_length=50, verbose_name='Theme Level'),
        ),
    ]