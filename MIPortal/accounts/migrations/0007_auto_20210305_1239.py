# Generated by Django 3.1.7 on 2021-03-05 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_customuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.TextField(max_length=50, unique=True),
        ),
    ]
