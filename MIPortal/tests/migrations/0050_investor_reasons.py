# Generated by Django 3.1.7 on 2021-04-19 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investors', '0003_auto_20210419_1053'),
        ('tests', '0049_auto_20210413_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor_Reasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('investor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Investors.investor')),
            ],
        ),
    ]
