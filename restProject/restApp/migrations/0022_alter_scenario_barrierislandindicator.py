# Generated by Django 4.1.7 on 2023-06-16 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0021_foundationtypeid_scenario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='barrierIslandIndicator',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
