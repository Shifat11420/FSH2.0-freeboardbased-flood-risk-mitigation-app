# Generated by Django 4.1.1 on 2022-09-28 16:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipCode', models.CharField(default=0, max_length=10)),
                ('streetNum', models.IntegerField()),
                ('streetName', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=20)),
                ('parishId', models.IntegerField()),
                ('firstFloorHeight', models.FloatField()),
                ('floodLocation', models.FloatField()),
                ('floodScale', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sampledatamodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('alias', models.CharField(max_length=60)),
                ('data', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='unitcost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipCode', models.CharField(max_length=10)),
                ('constructionCost', models.FloatField()),
                ('movingCost', models.FloatField()),
                ('lodgingRate', models.FloatField()),
            ],
        )
    ]