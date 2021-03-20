# Generated by Django 3.1.7 on 2021-03-20 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0021_financial_calculations_int_coverage_ration_ly'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial_calculations',
            name='int_coverage_ration_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='int_coverage_ration_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='int_coverage_ration_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='int_coverage_ration_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
    ]