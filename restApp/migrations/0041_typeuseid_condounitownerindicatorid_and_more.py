# Generated by Django 4.1.7 on 2023-07-03 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0040_alter_scenario_typeofuseid'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeuseid',
            name='condoUnitOwnerIndicatorID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.condounitownerindicator'),
        ),
        migrations.AddField(
            model_name='typeuseid',
            name='singleFamilyHomeIndicatorID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.singlefamilyhomeindicator'),
        ),
    ]
