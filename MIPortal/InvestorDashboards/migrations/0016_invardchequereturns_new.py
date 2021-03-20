# Generated by Django 3.1.7 on 2021-03-16 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investors', '0002_entity_entitybusinessroimapping_entityinvestorrormapping_investor_invoice_transaction_wallet'),
        ('InvestorDashboards', '0015_auto_20210316_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvardchequeReturns_new',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_account_no', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_instances', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Investors.business')),
            ],
        ),
    ]
