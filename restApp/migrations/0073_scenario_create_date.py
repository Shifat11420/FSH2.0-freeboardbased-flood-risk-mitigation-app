# Generated by Django 4.1.7 on 2023-08-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0072_alter_scenario_returnperiod100y_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
