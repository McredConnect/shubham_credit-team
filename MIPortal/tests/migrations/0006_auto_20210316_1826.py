# Generated by Django 3.1.7 on 2021-03-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_auto_20210316_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_details_in_last_tweleve_months',
            name='date_of_transaction',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
