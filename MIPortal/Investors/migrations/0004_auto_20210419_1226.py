# Generated by Django 3.1.7 on 2021-04-19 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Investors', '0003_auto_20210419_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investor',
            name='investor_adhaar',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_adhaar_proof',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_authorised_user_adhaar',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_authorised_user_adhaar_proof',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_authorised_user_dob',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_authorised_user_pan',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_authorised_user_pan_proof',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_bank_account_ifsc_code',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_cin_llp_cert_no',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_cin_llp_cert_proof',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_deed_moa_and_aoa',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_pan',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='investor_pan_proof',
        ),
        migrations.AddField(
            model_name='investor',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='escrow_balance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_Aadhaar',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_Aadhaar_proof',
            field=models.FileField(blank=True, null=True, upload_to='investor_aadhaar_proof'),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_CIN_LLP_cert_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_CIN_LLP_cert_proof',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_NRI_proof',
            field=models.FileField(blank=True, null=True, upload_to='investor_NRI_proof'),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_PAN',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_PAN_proof',
            field=models.FileField(blank=True, null=True, upload_to='investor_pan_proof'),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_authorised_user_Aadhaar',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_authorised_user_Aadhaar_proof',
            field=models.FileField(blank=True, null=True, upload_to='investor_authorised_user_Aadhaar_proof'),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_authorised_user_DOB',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_authorised_user_PAN',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_authorised_user_PAN_proof',
            field=models.FileField(blank=True, null=True, upload_to='investor_authorised_user_PAN_proof'),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_bank_account_IFSC_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_cert_incorporation',
            field=models.FileField(blank=True, null=True, upload_to='investor_cert_incorporation'),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_deed_MOA_and_AOA',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_gs_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='investor_gst_proof',
            field=models.FileField(blank=True, null=True, upload_to='investor_gst_proof'),
        ),
        migrations.AddField(
            model_name='investor',
            name='pending_reason',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='investor',
            name='investor_authorised_user_email',
            field=models.EmailField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='investor',
            name='investor_email',
            field=models.EmailField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='investor',
            name='investor_id',
            field=models.CharField(blank=True, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='investor',
            name='investor_resolution',
            field=models.FileField(blank=True, null=True, upload_to='investor_resolution'),
        ),
        migrations.AlterModelTable(
            name='investor',
            table=None,
        ),
    ]
