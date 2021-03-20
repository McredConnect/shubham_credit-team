# Generated by Django 3.1.7 on 2021-03-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvestorDashboards', '0007_auto_20210303_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='file_AOA_MOA',
        ),
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='file_COI_LLP_certificate',
        ),
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='file_board_resolution',
        ),
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='file_business_profile',
        ),
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='file_company_address_proof',
        ),
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='file_pan_card',
        ),
        migrations.RemoveField(
            model_name='businessdetails_test',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='businessdetails_test',
            name='input_file',
            field=models.FileField(blank=True, null=True, upload_to='Business_detail'),
        ),
    ]
