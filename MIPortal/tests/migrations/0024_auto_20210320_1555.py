# Generated by Django 3.1.7 on 2021-03-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0023_auto_20210320_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_financing_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_financing_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_financing_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_financing_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_financing_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_investment_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_investment_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_investment_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_investment_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_investment_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_operation_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_operation_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_operation_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_operation_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='cash_flow_from_operation_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='long_debt_term_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='long_debt_term_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='long_debt_term_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='long_debt_term_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='long_debt_term_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='secured_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='secured_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='secured_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='secured_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='secured_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='short_term_borrow_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='short_term_borrow_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='short_term_borrow_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='short_term_borrow_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='short_term_borrow_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='unsecured_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='unsecured_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='unsecured_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='unsecured_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='unsecured_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
