# Generated by Django 3.1.7 on 2021-03-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0020_auto_20210320_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial_calculations',
            name='int_coverage_ration_ly',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
