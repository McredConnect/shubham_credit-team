# Generated by Django 3.1.7 on 2021-04-12 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0045_auto_20210412_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='GSTR_three',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gst_no', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_as_per_gstr_three', models.CharField(blank=True, max_length=100, null=True)),
                ('deviation_from_sale', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
