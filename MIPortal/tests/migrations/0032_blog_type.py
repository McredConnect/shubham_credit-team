# Generated by Django 3.1.7 on 2021-03-23 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0031_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]