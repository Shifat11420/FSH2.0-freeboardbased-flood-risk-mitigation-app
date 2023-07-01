# Generated by Django 4.1.7 on 2023-07-01 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0035_floor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='floor',
        ),
        migrations.AddField(
            model_name='scenario',
            name='floorID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.floor'),
        ),
    ]
