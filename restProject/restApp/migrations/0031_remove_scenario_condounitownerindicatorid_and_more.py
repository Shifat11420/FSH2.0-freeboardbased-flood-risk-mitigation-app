# Generated by Django 4.1.7 on 2023-06-26 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0030_scenario_buildingvalue_scenario_contentsvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='condoUnitOwnerIndicatorID',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='primaryResidenceIndicatorID',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='singleFamilyHomeIndicatorID',
        ),
        migrations.AlterField(
            model_name='foundationtypeid',
            name='Name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='annualFloodRisk',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='buildingCoverage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='buildingDeductible',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='buildingValue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='contentsCoverage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='contentsDeductible',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='contentsValue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='federalAssistanceID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.federalassistance'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='floodInsuranceID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.floodinsurance'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='floor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='foundationDesignID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.foundationdesignid'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='foundationTypeID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.foundationtypeid'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='homeConditionID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.homecondition'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='homeShapeID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.homeshape'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='investmentTypeID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.investmenttype'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='mortgageID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.mortgage'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='numOfStoriesID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.numofstories'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='priorClaimsID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.priorclaims'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='typeUseID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.typeuseid'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='userTypeID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restApp.usertypeid'),
        ),
    ]
