# Generated by Django 4.1.7 on 2023-07-03 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0048_remove_scenario_condounitownerindicatorid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='firstFloorHeight',
            field=models.FloatField(null=True),
        ),
    ]
