# Generated by Django 3.1.7 on 2021-03-22 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvestorDashboards', '0018_auto_20210316_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerdetails',
            name='average_monthly_sale1',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='total_annual_sale1',
        ),
        migrations.AlterField(
            model_name='gstdetails_test',
            name='Todate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gstdetails_test',
            name='fromdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]