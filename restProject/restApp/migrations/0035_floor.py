# Generated by Django 4.1.7 on 2023-07-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0034_alter_scenario_floor'),
    ]

    operations = [
        migrations.CreateModel(
            name='floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
    ]
