# Generated by Django 3.1.7 on 2021-03-23 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InvestorDashboards', '0019_auto_20210322_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorisedperson_details',
            name='aadhaar',
        ),
        migrations.RemoveField(
            model_name='authorisedperson_details',
            name='pan',
        ),
    ]