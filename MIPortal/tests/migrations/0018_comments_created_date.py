# Generated by Django 3.1.7 on 2021-03-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0017_auto_20210319_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
