# Generated by Django 4.1.7 on 2023-07-01 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0033_crsrating_scenario_crsrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='floor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.floorsofinterest'),
        ),
    ]
