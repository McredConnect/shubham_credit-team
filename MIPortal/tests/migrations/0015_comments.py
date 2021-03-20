# Generated by Django 3.1.7 on 2021-03-19 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investors', '0002_entity_entitybusinessroimapping_entityinvestorrormapping_investor_invoice_transaction_wallet'),
        ('tests', '0014_gst_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Investors.business')),
            ],
        ),
    ]
