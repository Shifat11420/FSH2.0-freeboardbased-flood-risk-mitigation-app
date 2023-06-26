# Generated by Django 4.1.7 on 2023-06-26 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0031_remove_scenario_condounitownerindicatorid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='condoUnitOwnerIndicatorID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.condounitownerindicator'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='primaryResidenceIndicatorID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.primaryresidenceindicator'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='singleFamilyHomeIndicatorID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.singlefamilyhomeindicator'),
        ),
    ]
