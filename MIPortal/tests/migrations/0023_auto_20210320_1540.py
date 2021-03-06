# Generated by Django 3.1.7 on 2021-03-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0022_auto_20210320_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial_calculations',
            name='networth_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='networth_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='networth_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='networth_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='networth_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
