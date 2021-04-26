# Generated by Django 3.1.7 on 2021-03-16 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvestorDashboards', '0017_auto_20210316_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerdetails',
            name='average_monthly_sale',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='total_annual_sale',
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='average_monthly_sale1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='total_annual_sale1',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
