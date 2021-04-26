# Generated by Django 3.1.7 on 2021-03-16 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investors', '0002_entity_entitybusinessroimapping_entityinvestorrormapping_investor_invoice_transaction_wallet'),
        ('tests', '0004_top_ten_credits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='top_ten_credits',
            name='date_of_transaction',
        ),
        migrations.AddField(
            model_name='top_ten_credits',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emi_payement_details',
            name='date_of_transaction',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Top_ten_debits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_account_no', models.CharField(blank=True, max_length=100, null=True)),
                ('entity_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emi_amount', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Investors.business')),
            ],
        ),
    ]
