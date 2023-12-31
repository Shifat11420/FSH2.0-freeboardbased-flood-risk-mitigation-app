# Generated by Django 4.1.7 on 2023-07-24 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0059_stateabbreviation_scenario_lattitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ddfBuilding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.FloatField()),
                ('associatedDamage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ddfContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.FloatField()),
                ('associatedDamage', models.FloatField()),
            ],
        ),
    ]
