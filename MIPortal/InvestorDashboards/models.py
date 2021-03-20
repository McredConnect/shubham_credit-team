from django.db import models
# Create your models here.
from Investors.models import Business

class AuthorisedPerson_details(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    # aadhaar = models.FileField(upload_to="user_aadhaar", null=True, blank=True)
    # pan = models.FileField(upload_to="user_pan", null=True, blank=True)

class BusinessDetails_test(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    input_file = models.FileField(upload_to="Business_detail", null=True, blank=True)

class BankstatementDetails_test(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    AC_No = models.IntegerField(null=True, blank=True)
    AC_Type = models.CharField(max_length=100, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    To_date = models.DateField(null=True, blank=True)
    input_file = models.FileField(upload_to="Bankstatementdetail", null=True, blank=True)

class GSTDetails_test(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    gst_type = models.CharField(max_length=100, null=True, blank=True)
    gst_No = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    fromdate = models.DateField(null=True, blank=True)
    Todate = models.DateField(null=True, blank=True)
    input_file = models.FileField(upload_to="Gstdetail", null=True, blank=True)

class Financialdetail_test(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    statement_type = models.CharField(max_length=100, null=True, blank=True)
    from_date = models.DateField()
    To_date = models.DateField()
    input_file = models.FileField(upload_to="financialdetail", null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

class Analysisreports(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    nameofcompany = models.CharField(max_length=100, null=True, blank=True)
    filetype = models.CharField(max_length=100, null=True, blank=True)
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    report = models.FileField(upload_to="Analysisreports", null=True, blank=True)

class Customerdetails(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    per_tweleve_month_sale = models.IntegerField(null=True, blank=True)
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    input_file = models.FileField(upload_to="Customerdetails", null=True, blank=True)
    # average_monthly_sale1 = models.IntegerField(null=True, blank=True)
    # total_annual_sale1 = models.IntegerField(null=True, blank=True)

class Suppliersdetails(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    purchase = models.CharField(max_length=100, null=True, blank=True)
    last_tweleve_month_sale = models.CharField(max_length=100, null=True, blank=True)
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    input_file = models.FileField(upload_to="Suppliersdetails",null=True,blank=True)

class Shareholding(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    nameofshareholder = models.CharField(max_length=100, null=True, blank=True)
    percentage_of_shareholding = models.IntegerField(null=True, blank=True)
    input_file = models.FileField(upload_to="Shareholdings", null=True, blank=True)

class KYCdetail(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    Name_of_directors = models.CharField(max_length=100, null=True, blank=True)
    Type_of_ID = models.CharField(max_length=100, null=True, blank=True)
    ID_NO = models.IntegerField(null=True, blank=True)
    input_file = models.FileField(upload_to="KYCdetail", null=True, blank=True)

class CreditRating(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    ratingagency = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    date_of_rating = models.DateTimeField()
    amount_of_rating = models.IntegerField(null=True, blank=True)
    input_file = models.FileField(upload_to="Creditrating", null=True, blank=True)

class DebtProfile(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    name_of_lender = models.CharField(max_length=100, null=True, blank=True)
    type_of_loan = models.CharField(max_length=100, null=True, blank=True)
    amount_of_loan = models.CharField(max_length=100, null=True, blank=True)
    outstanding_amount = models.CharField(max_length=100, null=True, blank=True)
    rate_of_interest = models.CharField(max_length=100, null=True,blank=True)
    # type_of_limit = models.CharField(max_length=100, null=True, blank=True)
    # total_limit = models.IntegerField(null=True, blank=True)
    input_file = models.FileField(upload_to="Debtprofile", null=True, blank=True)

class BusinessProfile(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    brief = models.TextField()
    input_file = models.FileField(upload_to="BusinessProfile", null=True, blank=True)

class As26detail(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    name_of_document = models.CharField(max_length=100, null=True,blank=True)
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    input_file = models.FileField(upload_to="As26detail", null=True, blank=True)

class InvardchequeReturns(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    bank_account_no = models.CharField(max_length=100, null=True, blank=True)
    number_of_instances = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

class InvardchequeReturns_new(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    bank_account_no = models.CharField(max_length=100, null=True, blank=True)
    number_of_instances = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)


