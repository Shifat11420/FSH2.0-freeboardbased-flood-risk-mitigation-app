# Generated by Django 4.1.7 on 2023-07-03 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0045_foundationtypes_foundationdesignfortype'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='userTypeID',
            new_name='userType',
        ),
    ]
