# Generated by Django 4.1.7 on 2023-07-26 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0062_alter_scenario_homeshapeid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='homeShapeID',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='restApp.homeshape'),
        ),
    ]