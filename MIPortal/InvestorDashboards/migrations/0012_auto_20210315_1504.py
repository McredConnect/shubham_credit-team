# Generated by Django 3.1.7 on 2021-03-15 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investors', '0002_entity_entitybusinessroimapping_entityinvestorrormapping_investor_invoice_transaction_wallet'),
        ('InvestorDashboards', '0011_auto_20210308_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvardchequeReturns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_account_no', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_instances', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Investors.business')),
            ],
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='average_monthly_sale',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='total_annual_sale',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financialdetail_test',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bankstatementdetails_test',
            name='To_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bankstatementdetails_test',
            name='from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='GSTDetails_test',
        ),
    ]