# Generated by Django 4.1.7 on 2023-07-03 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0043_typeuseid_condounitownerindicatorid_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='foundationDesignID',
            new_name='foundationDesigns',
        ),
        migrations.RenameModel(
            old_name='foundationTypeID',
            new_name='foundationTypes',
        ),
    ]
