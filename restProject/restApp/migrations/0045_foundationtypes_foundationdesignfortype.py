# Generated by Django 4.1.7 on 2023-07-03 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0044_rename_foundationdesignid_foundationdesigns_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='foundationtypes',
            name='foundationDesignforType',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.foundationdesigns'),
        ),
    ]
