# Generated by Django 4.1.1 on 2023-04-14 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0011_alter_riskrating2results_coastalerosonbuldings_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='floorsOfInterest',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('homeIndicator', models.CharField(max_length=20)),
                ('ownerIndicator', models.CharField(max_length=20)),
                ('interest', models.CharField(max_length=20)),
                ('allExclCE', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='foundationType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('foundationtypes', models.CharField(max_length=60)),
                ('allExclCE', models.FloatField()),
                ('inlandFlood', models.FloatField()),
                ('stormSurge', models.FloatField()),
                ('tsunami', models.FloatField()),
                ('greatLakes', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='typeOfUSe',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('typeofuse', models.CharField(max_length=60)),
                ('flood', models.FloatField()),
                ('surge', models.FloatField()),
                ('tsunami', models.FloatField()),
                ('lakes', models.FloatField()),
            ],
        ),
    ]
