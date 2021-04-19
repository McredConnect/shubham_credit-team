# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from accounts.models import *


class Entity(models.Model):
    entity_id = models.CharField(primary_key=True, max_length=50)
    entity_name = models.CharField(max_length=20, blank=True, null=True)
    entity_address = models.CharField(max_length=30, blank=True, null=True)
    entity_contact_no = models.CharField(max_length=15, blank=True, null=True)
    entity_email_id = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_name_1 = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_email_1 = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_number_1 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_mobile_1 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_designation_1 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_name_2 = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_email_2 = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_number_2 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_mobile_2 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_designation_2 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_name_3 = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_email_3 = models.CharField(max_length=25, blank=True, null=True)
    entity_contact_person_number_3 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_mobile_3 = models.CharField(max_length=15, blank=True, null=True)
    entity_contact_person_designation_3 = models.CharField(max_length=15, blank=True, null=True)
    entity_sector = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    about_client = models.TextField(blank=True, null=True)
    credit_rating = models.CharField(max_length=30, blank=True, null=True)
    financial_detail = models.CharField(max_length=100, blank=True, null=True)
    payment_on_time = models.IntegerField(blank=True, null=True)
    total_invoices = models.IntegerField(blank=True, null=True)
    total_years = models.CharField(max_length=30, blank=True, null=True)
    company_overview = models.TextField(blank=True, null=True)
    history_with_mcred = models.TextField(blank=True, null=True)
    mcred_opinion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investors_entity'


class Business(models.Model):
    id = models.IntegerField()
    business_id = models.CharField(primary_key=True, max_length=50)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    cin_llp_no = models.CharField(db_column='CIN_LLP_no', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type_of_business = models.CharField(max_length=20, blank=True, null=True)
    sector = models.CharField(max_length=20, blank=True, null=True)
    bank_account_detail = models.CharField(max_length=20, blank=True, null=True)
    business_face_value_discount_rate = models.FloatField(blank=True, null=True)
    gst_detail = models.CharField(max_length=20, blank=True, null=True)
    as_26_detail = models.CharField(db_column='AS_26_detail', max_length=20, blank=True, null=True)  # Field name made lowercase.
    business_pan_card = models.CharField(max_length=16, blank=True, null=True)
    business_udyog_adhaar = models.CharField(max_length=16, blank=True, null=True)
    business_credit_rating = models.CharField(max_length=10, blank=True, null=True)
    business_financial_statement = models.CharField(max_length=20, blank=True, null=True)
    business_shareholding = models.CharField(max_length=20, blank=True, null=True)
    business_list_of_directors = models.CharField(max_length=20, blank=True, null=True)
    business_credit_report = models.CharField(max_length=20, blank=True, null=True)
    business_debt_profile = models.CharField(max_length=20, blank=True, null=True)
    business_customers = models.CharField(max_length=100, blank=True, null=True)
    business_suppliers = models.CharField(max_length=100, blank=True, null=True)
    business_aoa_moa = models.CharField(db_column='business_AOA_MOA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    business_address_proof = models.CharField(max_length=100, blank=True, null=True)
    business_board_resolution = models.CharField(max_length=20, blank=True, null=True)
    business_coi_deed = models.CharField(db_column='business_COI_Deed', max_length=100, blank=True, null=True)  # Field name made lowercase.
    business_gumasta = models.CharField(db_column='business_Gumasta', max_length=100, blank=True, null=True)  # Field name made lowercase.
    business_description = models.CharField(max_length=100, blank=True, null=True)
    business_contact_no = models.CharField(max_length=15, blank=True, null=True)
    business_address = models.CharField(max_length=100, blank=True, null=True)
    business_email_id = models.CharField(max_length=25, blank=True, null=True)
    business_user_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    business_user_email_id = models.CharField(max_length=25, blank=True, null=True)
    business_user_name = models.CharField(max_length=20, blank=True, null=True)
    business_user_pan_card = models.CharField(max_length=25, blank=True, null=True)
    business_user_adhaar_card = models.CharField(max_length=25, blank=True, null=True)
    business_user_dob = models.DateField(blank=True, null=True)
    partner_referal_code = models.CharField(max_length=20, blank=True, null=True)
    business_bank_account_no = models.CharField(max_length=20, blank=True, null=True)
    business_bank_account_cancelled_cheque = models.CharField(max_length=20, blank=True, null=True)
    business_bank_account_ifsc_code = models.CharField(db_column='business_bank_account_IFSC_code', max_length=10, blank=True, null=True)  # Field name made lowercase.
    business_bank_name = models.CharField(max_length=20, blank=True, null=True)
    business_mcred_wallet_acc_no = models.CharField(max_length=20, blank=True, null=True)
    business_mcred_wallet_bank_name = models.CharField(max_length=20, blank=True, null=True)
    assigned_sales_person = models.CharField(max_length=30, blank=True, null=True)
    facility_approved_amount = models.IntegerField(blank=True, null=True)
    entity_mapped = models.CharField(max_length=100, blank=True, null=True)
    facility_validity = models.CharField(max_length=100, blank=True, null=True)
    penal_interest_charges = models.IntegerField(blank=True, null=True)
    margin_period = models.CharField(max_length=100, blank=True, null=True)
    status_of_compliance = models.CharField(max_length=100, blank=True, null=True)
    status_of_due_clearance = models.CharField(max_length=100, blank=True, null=True)
    bank_statement_analysis_report = models.TextField(blank=True, null=True)
    gst_statement_analysis_report = models.TextField(blank=True, null=True)
    facility_assessment_report = models.TextField(blank=True, null=True)
    credit_analysis_report = models.TextField(blank=True, null=True)
    available_facility_limit = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    delay = models.CharField(max_length=50, blank=True, null=True)
    financials = models.CharField(max_length=100, blank=True, null=True)
    since_active = models.CharField(max_length=10, blank=True, null=True)
    total_invoices = models.IntegerField(blank=True, null=True)
    verified_items = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    company_overview = models.TextField(blank=True, null=True)
    history_with_mcred = models.TextField(blank=True, null=True)
    mcred_opinion = models.TextField(blank=True, null=True)
    business_profile_brief_description = models.CharField(max_length=100)
    pending_reason = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    turnover = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    year_of_incorporation = models.IntegerField(null=True,blank=True)
    plant_location = models.CharField(max_length=50,null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'investors_business'


# class Investor(models.Model):
#     investor_name = models.CharField(max_length=50, blank=True, null=True)
#     investor_category = models.CharField(max_length=20, blank=True, null=True)
#     investor_email = models.CharField(max_length=40, blank=True, null=True)
#     contact_no = models.CharField(max_length=15, blank=True, null=True)
#     investor_pan = models.CharField(db_column='investor_PAN', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     investor_Aadhaar = models.CharField(db_column='investor_Adhaar', max_length=16, blank=True, null=True)  # Field name made lowercase.
#     investor_pan_proof = models.CharField(db_column='investor_PAN_proof', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     investor_adhaar_proof = models.CharField(db_column='investor_Adhaar_proof', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     investor_gst_detail = models.CharField(max_length=25, blank=True, null=True)
#     investor_date_of_incorporation = models.DateField(blank=True, null=True)
#     investor_authorised_user_name = models.CharField(max_length=25, blank=True, null=True)
#     investor_authorised_user_mobile = models.CharField(max_length=15, blank=True, null=True)
#     investor_authorised_user_dob = models.DateField(db_column='investor_authorised_user_DOB', blank=True, null=True)  # Field name made lowercase.
#     investor_authorised_user_email = models.CharField(max_length=30, blank=True, null=True)
#     investor_authorised_user_address = models.CharField(max_length=50, blank=True, null=True)
#     investor_authorised_user_pan = models.CharField(db_column='investor_authorised_user_PAN', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     investor_authorised_user_adhaar = models.CharField(db_column='investor_authorised_user_Adhaar', max_length=16, blank=True, null=True)  # Field name made lowercase.
#     investor_authorised_user_pan_proof = models.CharField(db_column='investor_authorised_user_PAN_proof', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     investor_authorised_user_adhaar_proof = models.CharField(db_column='investor_authorised_user_Adhaar_proof', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     investor_cin_llp_cert_no = models.CharField(db_column='investor_CIN_LLP_cert_no', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     investor_cin_llp_cert_proof = models.CharField(db_column='investor_CIN_LLP_cert_proof', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     investor_deed_moa_and_aoa = models.CharField(db_column='investor_deed_MOA_and_AOA', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     investor_resolution = models.CharField(max_length=50, blank=True, null=True)
#     partner_referal_code = models.CharField(max_length=15, blank=True, null=True)
#     investor_bank_account_no = models.CharField(max_length=20, blank=True, null=True)
#     investor_bank_account_cancelled_cheque = models.CharField(max_length=15, blank=True, null=True)
#     investor_bank_account_ifsc_code = models.CharField(db_column='investor_bank_account_IFSC_code', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     investor_bank_name = models.CharField(max_length=30, blank=True, null=True)
#     investor_mcred_wallet_account_no = models.CharField(max_length=20, blank=True, null=True)
#     investor_mcred_wallet_bank_name = models.CharField(max_length=25, blank=True, null=True)
#     special_status_to_investor = models.CharField(max_length=30, blank=True, null=True)
#     special_applicable_yield = models.FloatField(blank=True, null=True)
#     minimum_investment_limit = models.FloatField(blank=True, null=True)
#     expected_yield = models.FloatField(blank=True, null=True)
#     investor_id = models.CharField(primary_key=True, max_length=50)
#     user_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'investors_investor'

class Investor(models.Model):
    investor_id = models.CharField(max_length=50, primary_key=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    investor_name = models.CharField(max_length=50, null=True, blank=True)
    investor_category = models.CharField(max_length=20, null=True, blank=True)
    investor_email = models.EmailField(max_length=40, null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    investor_PAN = models.CharField(max_length=15, null=True, blank=True)
    investor_Aadhaar = models.CharField(max_length=16, null=True, blank=True)
    investor_PAN_proof = models.FileField(upload_to='investor_pan_proof', null=True, blank=True)
    investor_Aadhaar_proof = models.FileField(upload_to='investor_aadhaar_proof', null=True, blank=True)
    investor_NRI_proof = models.FileField(upload_to='investor_NRI_proof', null=True, blank=True)
    investor_gst_detail = models.CharField(max_length=25, null=True, blank=True)
    investor_gs_number = models.CharField(max_length=15, null=True,  blank=True)
    investor_gst_proof = models.FileField(upload_to='investor_gst_proof', null=True, blank=True)
    investor_date_of_incorporation = models.DateField(null=True, blank=True)
    investor_authorised_user_name = models.CharField(max_length=25, null=True, blank=True)
    investor_authorised_user_mobile = models.CharField(max_length=15, null=True, blank=True)
    investor_authorised_user_DOB = models.DateField(null=True, blank=True)
    investor_authorised_user_email = models.EmailField(max_length=30, null=True, blank=True)
    investor_authorised_user_address = models.CharField(max_length=50, null=True, blank=True)
    investor_authorised_user_PAN = models.CharField(max_length=15, null=True, blank=True)
    investor_authorised_user_Aadhaar = models.CharField(max_length=16, null=True, blank=True)
    investor_authorised_user_PAN_proof = models.FileField(upload_to='investor_authorised_user_PAN_proof', null=True, blank=True)
    investor_authorised_user_Aadhaar_proof = models.FileField(upload_to='investor_authorised_user_Aadhaar_proof', null=True, blank=True)
    investor_CIN_LLP_cert_no = models.CharField(max_length=20, null=True, blank=True)
    investor_CIN_LLP_cert_proof = models.CharField(max_length=20, null=True, blank=True)
    investor_deed_MOA_and_AOA = models.CharField(max_length=50, null=True, blank=True)
    investor_resolution = models.FileField(upload_to='investor_resolution', null=True, blank=True)
    investor_cert_incorporation = models.FileField(upload_to='investor_cert_incorporation', null=True, blank=True)
    # investor_reg_partnership_deed = models.FileField(upload_to='investor_resolution', null=True, blank=True)

    partner_referal_code = models.CharField(max_length=15, null=True, blank=True)
    investor_bank_account_no = models.CharField(max_length=20, null=True, blank=True)
    investor_bank_account_cancelled_cheque = models.CharField(max_length=15, null=True, blank=True)
    investor_bank_account_IFSC_code = models.CharField(max_length=15, null=True, blank=True)
    investor_bank_name = models.CharField(max_length=30, null=True, blank=True)
    investor_mcred_wallet_account_no = models.CharField(max_length=20, null=True, blank=True)
    investor_mcred_wallet_bank_name = models.CharField(max_length=25, null=True, blank=True)
    special_status_to_investor = models.CharField(max_length=30, null=True, blank=True)
    special_applicable_yield = models.FloatField(null=True, blank=True)
    minimum_investment_limit = models.FloatField(null=True, blank=True)
    expected_yield = models.FloatField(null=True, blank=True)
    escrow_balance = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    pending_reason = models.CharField(max_length=50, null=True, blank=True)


class Invoice(models.Model):
    invoice_id = models.CharField(primary_key=True, max_length=50)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    business_id = models.ForeignKey(Business, on_delete=models.DO_NOTHING, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    invoice_upload_date = models.DateField(blank=True, null=True)
    entity_name = models.CharField(max_length=50, blank=True, null=True)
    batch_invoice_amount = models.FloatField(blank=True, null=True)
    invoice_amount = models.FloatField(blank=True, null=True)
    batch_number_of_invoices = models.IntegerField(blank=True, null=True)
    batch_no = models.CharField(max_length=10, blank=True, null=True)
    applicable_roi = models.FloatField(db_column='applicable_ROI', blank=True, null=True)  # Field name made lowercase.
    applicable_discount_rate = models.FloatField(blank=True, null=True)
    invoice_fundable_amount = models.FloatField(blank=True, null=True)
    invoice_investment_amount = models.FloatField(blank=True, null=True)
    invoice_total_investment = models.FloatField(blank=True, null=True)
    invoice_due_date = models.DateField(blank=True, null=True)
    ewb_id = models.CharField(db_column='EWB_id', max_length=20, blank=True, null=True)  # Field name made lowercase.
    product_description = models.CharField(max_length=50, blank=True, null=True)
    product_hsn_code = models.CharField(db_column='product_HSN_code', max_length=10, blank=True, null=True)  # Field name made lowercase.
    credit_period_as_per_agreement = models.IntegerField(blank=True, null=True)
    business_over_due_pending = models.FloatField(blank=True, null=True)
    tds_applicable_on_invoice = models.FloatField(blank=True, null=True)
    assignment_of_invoice = models.CharField(max_length=100, blank=True, null=True)
    invoice_assigned_to = models.CharField(max_length=100, blank=True, null=True)
    po_number = models.CharField(db_column='PO_number', max_length=50, blank=True, null=True)  # Field name made lowercase.
    validity_of_po = models.DateField(db_column='validity_of_PO', blank=True, null=True)  # Field name made lowercase.
    gst_amount = models.FloatField(blank=True, null=True)
    igst = models.FloatField(blank=True, null=True)
    cgst = models.FloatField(blank=True, null=True)
    sgst = models.FloatField(blank=True, null=True)
    bank_detail_in_invoice = models.CharField(max_length=25, blank=True, null=True)
    available_limit_to_business = models.FloatField(blank=True, null=True)
    validity_of_invoice = models.DateField(blank=True, null=True)
    final_approval_status_verification = models.CharField(max_length=30, blank=True, null=True)
    applicable_gst_rate = models.FloatField(blank=True, null=True)
    invoice_live_date = models.DateField(blank=True, null=True)
    invoice_approval_date = models.DateField(blank=True, null=True)
    goods_delivery_date = models.DateField(blank=True, null=True)
    invoice_subscription_status = models.FloatField(blank=True, null=True)
    invoice_available_investment = models.FloatField(blank=True, null=True)
    margin_days = models.IntegerField(blank=True, null=True)
    goods_delivery_sts = models.CharField(max_length=50, blank=True, null=True)
    transporter_name = models.CharField(max_length=20, blank=True, null=True)
    transporter_vehicle_no = models.CharField(max_length=20, blank=True, null=True)
    goods_origin_state = models.CharField(max_length=20, blank=True, null=True)
    goods_delivery_state = models.CharField(max_length=20, blank=True, null=True)
    invoice_pdf_link = models.CharField(max_length=100, blank=True, null=True)
    invoice_pdf = models.CharField(max_length=100, blank=True, null=True)
    ewb_no = models.CharField(db_column='EWB_no', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_entered_total_invoice_amount = models.FloatField(blank=True, null=True)
    ror_for_investor = models.FloatField(blank=True, null=True)
    maturity_after_investment = models.FloatField(blank=True, null=True)
    amount_due_investor = models.FloatField(blank=True, null=True)
    expected_gross_yield = models.FloatField(blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investors_invoice'


class Transaction(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING, blank=True, null=True)
    invoice_upload_date = models.DateField(blank=True, null=True)
    batch_no = models.CharField(max_length=10, blank=True, null=True)
    transaction_date = models.DateField(blank=True, null=True)
    amount_invested = models.FloatField(blank=True, null=True)
    platform_service_fee_investor = models.FloatField(blank=True, null=True)
    gst_on_platform_service_fee_investor = models.FloatField(blank=True, null=True)
    amount_debited_from_investor_wallet = models.FloatField(blank=True, null=True)
    tenor = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    applicable_yield_investor = models.FloatField(blank=True, null=True)
    applicable_roi = models.FloatField(db_column='applicable_ROI', blank=True, null=True)  # Field name made lowercase.
    amount_settled_with_business = models.FloatField(blank=True, null=True)
    business_id = models.ForeignKey(Business, on_delete=models.DO_NOTHING, blank=True, null=True)
    investor_id = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, blank=True, null=True)
    entity_id = models.CharField(max_length=50, blank=True, null=True)
    entity_name = models.CharField(max_length=100, blank=True, null=True)
    investor_business_agreement = models.CharField(max_length=100, blank=True, null=True)
    platform_service_fee_business = models.FloatField(blank=True, null=True)
    gst_on_platform_service_fee_business = models.FloatField(blank=True, null=True)
    amount_to_be_credited_in_business_wallet = models.FloatField(blank=True, null=True)
    repayment_amount = models.FloatField(blank=True, null=True)
    settlement_amount_with_investor = models.FloatField(blank=True, null=True)
    settlement_amount_with_business = models.FloatField(blank=True, null=True)
    tds_on_investor_fee = models.FloatField(db_column='TDS_on_investor_fee', blank=True, null=True)  # Field name made lowercase.
    tds_on_business_fee = models.FloatField(db_column='TDS_on_business_fee', blank=True, null=True)  # Field name made lowercase.
    transaction_type = models.CharField(max_length=50)
    invoice_pk = models.CharField(max_length=25, blank=True, null=True)
    calculated_yield = models.FloatField(blank=True, null=True)
    transaction_id = models.CharField(primary_key=True, max_length=50)
    transaction_sub_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'investors_transaction'


class Wallet(models.Model):
    business_id = models.CharField(max_length=100, blank=True, null=True)
    investor_id = models.CharField(max_length=100, blank=True, null=True)
    entity_id = models.CharField(max_length=100, blank=True, null=True)
    business_wallet_account = models.CharField(max_length=100, blank=True, null=True)
    investor_wallet_account = models.CharField(max_length=100, blank=True, null=True)
    amount_debit_from_investor_wallet = models.CharField(max_length=50, blank=True, null=True)
    amount_debit_from_business_wallet = models.CharField(max_length=50, blank=True, null=True)
    amount_credit_from_investor_wallet = models.CharField(max_length=50, blank=True, null=True)
    amount_credit_from_business_wallet = models.CharField(max_length=50, blank=True, null=True)
    amount_credit_to_mcred_wallet = models.CharField(max_length=50, blank=True, null=True)
    date_of_debit = models.DateField(blank=True, null=True)
    date_of_credit = models.DateField(blank=True, null=True)
    amount_credit_from_entity_bank_account = models.CharField(max_length=50, blank=True, null=True)
    investor_funds_wallet_to_bank_account = models.CharField(max_length=50, blank=True, null=True)
    investor_funds_bank_account_to_wallet = models.CharField(max_length=50, blank=True, null=True)
    business_funds_wallet_to_bank_account = models.CharField(max_length=50, blank=True, null=True)
    business_funds_bank_account_to_wallet = models.CharField(max_length=50, blank=True, null=True)
    purpose = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investors_wallet'


class EntityBusinessROIMapping(models.Model):
    entity_id = models.ForeignKey(Entity,on_delete=models.DO_NOTHING, blank=True, null=True)
    applicable_roi = models.FloatField(blank=True, null=True)
    benchmark_roi = models.FloatField(blank=True, null=True)
    special_roi = models.FloatField(blank=True, null=True)
    sector_base_rate = models.FloatField(blank=True, null=True)
    sector_risk_premium = models.FloatField(blank=True, null=True)
    business_risk_premium = models.FloatField(blank=True, null=True)
    entity_risk_premium = models.FloatField(blank=True, null=True)
    business_id = models.ForeignKey(Business, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investors_entitybusinessroimapping'


class EntityInvestorRORMapping(models.Model):
    investor_id = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, blank=True, null=True)
    entity_id = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, blank=True, null=True)
    applicable_ror = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investors_entityinvestorrormapping'
