# Generated by Django 4.1.7 on 2023-07-11 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0057_remove_scenario_mortgageid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='floor1to100ID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='restApp.floor1to100'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='floor1to3ID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='restApp.floor1to3'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='floor1to4ID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='restApp.floor1to4'),
        ),
    ]
