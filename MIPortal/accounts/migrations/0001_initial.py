# Generated by Django 3.1.7 on 2021-03-02 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountsCustomuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.CharField(blank=True, max_length=30, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'accounts_customuser',
                'managed': False,
            },
        ),
    ]