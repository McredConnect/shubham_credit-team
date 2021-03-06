# Generated by Django 3.1.7 on 2021-03-22 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investors', '0002_entity_entitybusinessroimapping_entityinvestorrormapping_investor_invoice_transaction_wallet'),
        ('tests', '0027_kycdetail_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebtProfile_new',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_lender', models.CharField(blank=True, max_length=100, null=True)),
                ('type_of_loan', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_of_loan', models.CharField(blank=True, max_length=100, null=True)),
                ('outstanding_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('rate_of_interest', models.CharField(blank=True, max_length=100, null=True)),
                ('type_of_limit', models.CharField(blank=True, max_length=100, null=True)),
                ('total_limit', models.IntegerField(blank=True, null=True)),
                ('input_file', models.FileField(blank=True, null=True, upload_to='Debtprofile')),
                ('business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Investors.business')),
            ],
        ),
    ]
