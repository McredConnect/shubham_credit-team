# Generated by Django 3.1.7 on 2021-03-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0018_comments_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial_calculations',
            name='interest_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='interest_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='interest_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='interest_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='interest_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pat_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pat_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pat_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pat_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pat_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pbt_cy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pbt_lqy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pbt_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pbt_py',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financial_calculations',
            name='pbt_sqy',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
