# Generated by Django 4.1.1 on 2023-03-30 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0008_riskrating2results'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riskrating2results',
            old_name='psunamiBuldings',
            new_name='tsunamiBuldings',
        ),
        migrations.RenameField(
            model_name='riskrating2results',
            old_name='psunamiContents',
            new_name='tsunamiContents',
        ),
    ]