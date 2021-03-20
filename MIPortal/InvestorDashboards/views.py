from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from Investors.models import *
from tests.models import *


def bank_detail(request):
    business_id = request.session['business_id']
    print("In bank detail", business_id)
    objs = BankstatementDetails_test.objects.filter(business_id=business_id)
    inverd_cheque = InvardchequeReturns.objects.filter(business_id=business_id)
    debit_credit_objs = Debit_credit_same_party.objects.filter(business_id=business_id)
    loan_detail_obj = Loan_details_in_last_tweleve_months.objects.filter(business_id=business_id)
    emi_obj = EMI_payement_details.objects.filter(business_id=business_id)
    credit_obj = Top_ten_credits.objects.filter(business_id=business_id)
    debits_obj = Top_ten_debits.objects.filter(business_id=business_id)
    comments_obj = Comments.objects.filter(type="bankdetail") & Comments.objects.filter(business_id=business_id)
    print("comments_obj",comments_obj)
    print("in bankdetail", objs)
    context = {'objs': objs, 'business_id':business_id, 'inverd_cheque':inverd_cheque, 'debit_credit_objs':debit_credit_objs, 'loan_detail_obj':loan_detail_obj, 'emi_obj':emi_obj, 'credit_obj':credit_obj, 'debits_obj':debits_obj,'comments_obj':comments_obj}
    if request.method == "POST":
        bankname = request.POST.get('bankname')
        acctype = request.POST.get('acctype')
        accno = request.POST.get('accno')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        file = request.FILES['file1']
        business_obj = Business.objects.get(business_id=business_id)
        obj = BankstatementDetails_test.objects.create(bank_name=bankname, AC_No=accno, AC_Type=acctype,
                                                           from_date=fromdate, To_date=todate, input_file=file,business_id=business_obj)
        if obj:
            return redirect('bank_detail')
    return render(request, 'InvestorDashboards/test1.html', context)

def debt_profile(request):
    business_id = request.session['business_id']
    comments_obj = Comments.objects.filter(type="debtprofiledetail") & Comments.objects.filter(business_id=business_id)
    objs = DebtProfile.objects.filter(business_id=business_id)
    context = {'objs': objs, 'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        name_of_lender = request.POST.get('nameoflender')
        type_of_loan = request.POST.get('typeofloan')
        amount_of_loan = request.POST.get('amountofloan')
        outstanding_amount = request.POST.get('outstandingamount')
        rate_of_interest = request.POST.get('rateofinterest')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = DebtProfile.objects.create(name_of_lender = name_of_lender,type_of_loan = type_of_loan, amount_of_loan=amount_of_loan,outstanding_amount = outstanding_amount, rate_of_interest = rate_of_interest, input_file=input_file,business_id=business_obj)
        if obj:
            return redirect('debt_profile')
    return render(request, 'InvestorDashboards/debt_profile.html', context)

def credit_rating(request):
    business_id = request.session['business_id']
    print("In bank detail", business_id)
    objs = CreditRating.objects.filter(business_id=business_id)
    comments_obj = Comments.objects.filter(type="creditratingdetail") & Comments.objects.filter(business_id=business_id)
    print("in bankdetail", objs)
    context = {'objs': objs,'business_id': business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        ratingagency = request.POST.get('ratingagency')
        rating = request.POST.get('rating')
        date_of_rating = request.POST.get('dateofrating')
        amount_of_rating = request.POST.get('amountofrating')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = CreditRating.objects.create(ratingagency = ratingagency, rating = rating, date_of_rating =  date_of_rating, amount_of_rating = amount_of_rating, input_file = input_file,business_id=business_obj)
        if obj:
            return redirect('credit_rating')
    return render(request, 'InvestorDashboards/credit_rating.html', context)

def business_profile(request):
    business_id = request.session['business_id']
    print("In business profile", business_id)
    objs = BusinessProfile.objects.filter(business_id=business_id)
    print("in business profile", objs)
    context = {'objs': objs,'business_id': business_id}
    print("In business profile")
    if request.method == "POST":
        brief = request.POST.get('brief')
        print(brief)
        input_file = request.FILES['file']
        print(input_file)
        business_obj = Business.objects.get(business_id=business_id)
        print(business_obj)
        BusinessProfile_obj = BusinessProfile.objects.create(brief=brief,input_file=input_file,business_id=business_obj)
        if BusinessProfile_obj:
            return redirect('business_profile')
    return render(request, 'InvestorDashboards/business_profile.html',context)

def gst_detail(request):
    gst_number = request.session['gst_number']
    business_id = request.session['business_id']
    print("In gst detail", business_id)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    gst_num_obj = GSTDetails_new.objects.get(gst_No=gst_number)
    domestic_sale = gst_num_obj.domestic_sale
    print(domestic_sale)
    export_sale = gst_num_obj.export_sale
    print(export_sale)
    sales_as_per_gstr_thee = gst_num_obj.sales_as_per_gstr_thee
    deviation_from_sale = gst_num_obj.deviation_from_sale
    print(gst_num_obj)
    gst_sale_obj = GST_sale.objects.filter(gst_no=gst_number)
    gst_customer_obj = GST_customers.objects.filter(gst_no=gst_number)
    gst_suppliers_obj = GST_suppliers.objects.filter(gst_no=gst_number)
    gst_products_obj = GST_products.objects.filter(gst_no=gst_number)
    comments_obj = Comments.objects.filter(type="gstdetail") & Comments.objects.filter(business_id=business_id)
    print("In gst comments",comments_obj)
    gst_num = []

    objs = GSTDetails_new.objects.filter(business_id=business_id)
    print("here with",objs)
    for i in objs:
        val = i.gst_No
        gst_num.append(val)
    print("In gst details gst Num",gst_num)
    print("in gstdetail", objs)
    context = {'objs': objs,'business_id':business_id, 'gst_num':gst_num,'domestic_sale':domestic_sale,'export_sale':export_sale,'sales_as_per_gstr_thee':sales_as_per_gstr_thee,'deviation_from_sale':deviation_from_sale,'gst_sale_obj':gst_sale_obj,'gst_customer_obj':gst_customer_obj,'gst_suppliers_obj': gst_suppliers_obj,'gst_products_obj':gst_products_obj,'comments_obj':comments_obj}
    if request.method == "POST":
        gsttype = request.POST.get('gsttype')
        gstno = request.POST.get('gstno')
        state = request.POST.get('state')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = GSTDetails_new.objects.create(gst_type=gsttype, gst_No=gstno, state=state,
                                                           fromdate=fromdate, Todate=todate, input_file=file,business_id=business_obj)
        if obj:
            return redirect('gst_detail')
    return render(request, 'InvestorDashboards/gstdetail.html',context)

def financial_detail(request):
    business_id = request.session['business_id']
    print("In financial detail", business_id)
    objs = Financialdetail_test.objects.filter(business_id=business_id)
    comments_obj = Comments.objects.filter(type="financialdetail") & Comments.objects.filter(business_id=business_id)
    print("in financialdetail", objs)
    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        statementtype = request.POST.get('statementtype')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = Financialdetail_test.objects.create(statement_type=statementtype, from_date=fromdate, To_date=todate, input_file =file,business_id=business_obj)
        if obj:
            return redirect('financial_detail')
    return render(request, 'InvestorDashboards/financialdetail.html', context)

def business_detail(request, pk):
    print(pk)
    request.session['business_id'] = pk
    business_id = request.session['business_id']
    print("In business detail", business_id)
    objs = BusinessDetails_test.objects.filter(business_id=pk)
    print(objs)
    authorisedperson_obj = AuthorisedPerson_details.objects.filter(business_id=business_id)
    # {{objs.business_id.user_id.username}}
    print(authorisedperson_obj)
    comments_obj = Comments.objects.filter(type="businessdetail") & Comments.objects.filter(business_id=business_id)
    for i in objs:
        company = i.business_id.user_id.username
        # 'company': company,
        sector = i.business_id.sector
    context = {'objs': objs, 'sector': sector, 'business_id': business_id, 'company': company, 'authorisedperson_obj':authorisedperson_obj,'comments_obj':comments_obj}
    if request.method == "POST":
        file_type = request.POST.get('filetype')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=pk)
        obj = BusinessDetails_test.objects.create(file_name=file_type, input_file=input_file, business_id=business_obj)
        if obj:
            return redirect('business_detail', pk)

    return render(request, 'InvestorDashboards/businessdetail.html', context)

def analysis_report(request):
    business_id = request.session['business_id']
    print("In financial detail", business_id)
    objs = Analysisreports.objects.filter(business_id=business_id)
    print("in financialdetail", objs)
    comments_obj = Comments.objects.filter(type="analysisreport") & Comments.objects.filter(business_id=business_id)
    context = {'objs': objs,'business_id': business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        filetype = request.POST.get('typeofreport')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        report = request.FILES['file_reports']
        business_obj = Business.objects.get(business_id=business_id)
        obj = Analysisreports.objects.create(filetype=filetype, fromdate=fromdate, todate=todate,report=report,business_id=business_obj)
        if obj:
            return redirect('analysis_report')
    return render(request, 'InvestorDashboards/analysisreport.html', context)

def customer_detail(request):
    business_id = request.session['business_id']
    print("In customer_detail detail", business_id)
    objs = Customerdetails.objects.filter(business_id=business_id)
    print("in customer_detail", objs)
    comments_obj = Comments.objects.filter(type="customerdetail") & Comments.objects.filter(business_id=business_id)

    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        name = request.POST.get('name')
        per_tweleve_month_sale = request.POST.get('sale')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = Customerdetails.objects.create(name=name, per_tweleve_month_sale=per_tweleve_month_sale, fromdate=fromdate, todate=todate, input_file=input_file,business_id=business_obj)
        if obj:
            return redirect('customer_detail')
    return render(request, 'InvestorDashboards/customerdetail.html', context)

def supplier_detail(request):
    business_id = request.session['business_id']
    print("In customer_detail detail", business_id)
    objs = Suppliersdetails.objects.filter(business_id=business_id)
    print("in customer_detail", objs)
    comments_obj = Comments.objects.filter(type="supplierdetail") & Comments.objects.filter(business_id=business_id)
    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        print("IN if of supplier detail ")
        name = request.POST.get('name')
        print(name)
        purchase = request.POST.get('purchase')
        print(purchase)
        last_tweleve_month_sale = request.POST.get('sale')
        print(last_tweleve_month_sale)
        fromdate = request.POST.get('fromdate')
        print(fromdate)
        todate = request.POST.get('todate')
        print(todate)
        input_file = request.FILES['file']
        print(input_file)
        business_obj = Business.objects.get(business_id=business_id)
        obj = Suppliersdetails.objects.create(name=name, purchase=purchase, last_tweleve_month_sale=last_tweleve_month_sale, fromdate=fromdate,
                                              todate=todate, input_file=input_file,business_id=business_obj)
        print(obj)
        if obj:
            return redirect('supplier_detail')
    return render(request, 'InvestorDashboards/suppliers.html', context)

def shareholding_detail(request):
    business_id = request.session['business_id']
    print("In shareholding_detail detail", business_id)
    objs = Shareholding.objects.filter(business_id=business_id)
    print("in shareholding_detail", objs)
    comments_obj = Comments.objects.filter(type="shareholdingdetail") & Comments.objects.filter(business_id=business_id)
    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        nameofshareholder = request.POST.get('name')
        percentage_of_shareholding = request.POST.get('percentage')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = Shareholding.objects.create(nameofshareholder=nameofshareholder, percentage_of_shareholding=percentage_of_shareholding,input_file=input_file,business_id=business_obj)
        if obj:
            return redirect('shareholding_detail')
    return render(request, 'InvestorDashboards/shareholding.html', context)


def KYC_detail(request):
    business_id = request.session['business_id']
    print("In KYCdetail detail", business_id)
    objs = KYCdetail.objects.filter(business_id=business_id)
    print("in KYCdetail", objs)
    comments_obj = Comments.objects.filter(type="kycdetail") & Comments.objects.filter(business_id=business_id)
    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        Name_of_directors = request.POST.get('name')
        Type_of_ID = request.POST['typeofid']
        ID_NO = request.POST.get('ID_NO')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = KYCdetail.objects.create(Name_of_directors=Name_of_directors, Type_of_ID=Type_of_ID, ID_NO=ID_NO, input_file=input_file, business_id=business_obj)
        if obj:
            return redirect('KYC_detail')
    return render(request, 'InvestorDashboards/KYCdetail.html', context)

def authorisedperson_detail(request):
    business_id = request.session['business_id']
    if request.method == "POST":
        name = request.POST.get('name_authorised_person')
        location = request.POST.get('location')
        designation = request.POST.get('designation')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        mobile = request.POST.get('mobile')
        business_obj = Business.objects.get(business_id=business_id)
        obj = AuthorisedPerson_details.objects.create(name=name, location=location, designation=designation, email=email, phone=phone, mobile=mobile,business_id=business_obj)

    return redirect('business_detail', business_id)

def AS26_detail(request):
    business_id = request.session['business_id']
    # print("In KYCdetail detail", business_id)
    objs = As26detail.objects.filter(business_id=business_id)
    # print("in KYCdetail", objs)
    context = {'objs': objs,'business_id':business_id}
    if request.method == "POST":
        name_of_document = request.POST.get('name')
        fromdate = request.POST['fromdate']
        todate = request.POST.get('todate')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = As26detail.objects.create(name_of_document=name_of_document, fromdate=fromdate, todate=todate, input_file=input_file, business_id=business_obj)
        if obj:
            return redirect('AS26_detail')
    return render(request, 'InvestorDashboards/test1.html', context)


def removeobj(request, pk):
    business_id = request.session['business_id']
    print("business_id=", business_id)
    print(pk)
    BusinessDetails_test_obj = BusinessDetails_test.objects.filter(id=pk).first()
    if BusinessDetails_test_obj:
        BusinessDetails_test_obj.delete()
    return redirect('business_detail', business_id)

def removeobj_bankdetail(request, pk):
    BankstatementDetails_test_obj = BankstatementDetails_test.objects.filter(id=pk).first()
    if BankstatementDetails_test_obj:
        BankstatementDetails_test_obj.delete()
    return redirect('bank_detail')


def test(request):
    return render(request, "InvestorDashboards/test1.html")

def removeobj_financialdetail(request, pk):
    Financialdetail_test_obj = Financialdetail_test.objects.filter(id=pk).first()
    if Financialdetail_test_obj:
        Financialdetail_test_obj.delete()
    return redirect('financial_detail')

def removeobj_gstdetail(request, pk):
    GSTDetails_test_obj = GSTDetails_test.objects.filter(id=pk).first()
    if GSTDetails_test_obj:
        GSTDetails_test_obj.delete()
    return redirect('gst_detail')

def remove_authorisedperson(request, pk):
    business_id = request.session['business_id']
    AuthorisedPerson_details_obj = AuthorisedPerson_details.objects.filter(id=pk).first()
    if AuthorisedPerson_details_obj:
        AuthorisedPerson_details_obj.delete()
    return redirect('business_detail', business_id)

def remove_debt_profile(request, pk):
    DebtProfile_obj = DebtProfile.objects.filter(id=pk).first()
    if DebtProfile_obj:
        DebtProfile_obj.delete()
    return redirect('debt_profile')

def remove_analysisreport(request, pk):
    Analysisreports_obj = Analysisreports.objects.filter(id=pk).first()
    if Analysisreports_obj:
        Analysisreports_obj.delete()
    return redirect('analysis_report')

def remove_creditrating(request, pk):
    CreditRating_obj = CreditRating.objects.filter(id=pk).first()
    if CreditRating_obj:
        CreditRating_obj.delete()
    return redirect('credit_rating')

def remove_KYCdetail(request,pk):
    KYCdetail_obj = KYCdetail.objects.filter(id=pk).first()
    if KYCdetail_obj:
        KYCdetail_obj.delete()
    return redirect('KYC_detail')

def remove_shareholding(request, pk):
    Shareholding_obj = Shareholding.objects.filter(id=pk).first()
    if Shareholding_obj:
        Shareholding_obj.delete()
    return redirect('shareholding_detail')

def remove_suppliersdetails(request, pk):
    Suppliersdetails_obj = Suppliersdetails.objects.filter(id=pk).first()
    if Suppliersdetails_obj:
        Suppliersdetails_obj.delete()
    return redirect('supplier_detail')

def remove_customerdetail(request, pk):
    Customerdetails_obj = Customerdetails.objects.filter(id=pk).first()
    if Customerdetails_obj:
        Customerdetails_obj.delete()
    return redirect('customer_detail')

def remove_AS26detail(request, pk):
    As26detail_obj = As26detail.objects.filter(id=pk).first()
    if As26detail_obj:
        As26detail_obj.delete()
    return redirect('AS26_detail')

def business(request):
    print("In business view")
    objs = Business.objects.all()
    print(objs)
    context = {'objs':objs}
    return render(request, 'InvestorDashboards/business.html', context)

def pending_businesses(request):
    print("In business view")
    objs = Business.objects.filter(status="PENDING")
    print(objs)
    context = {'objs': objs}
    return render(request, 'InvestorDashboards/pending_businesses.html', context)

def registered_businesses(request):
    print("In business view")
    objs = Business.objects.filter(status="APPROVED")
    print(objs)
    context = {'objs': objs}
    return render(request, 'InvestorDashboards/registered_businesses.html', context)

def pending_form(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/pendingform.html', context)

def approved_form(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/approvedform.html', context)

def reason(request, pk):
    print("in REASON", pk)
    if request.method == "POST":
        message = request.POST.get('reason')
        print(message)
        business_obj = Business.objects.get(business_id=pk)
        print("BUSINESS OBJECTS IN REASON", business_obj)
        business_obj.status = "PENDING"
        business_obj.pending_reason = message
        business_obj.save()
    return redirect('pending_businesses')

def fascilate_amount(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/fascilateamountform.html', context)

def enter_fascilate_amount(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/fascilateamountform.html', context)

def fascilate_amount_save(request, pk):
    if request.method == "POST":
        amount = request.POST.get('amount')
        print(amount)
        business_obj = Business.objects.get(business_id=pk)
        print(business_obj)
        business_obj.status = "APPROVED"
        business_obj.facility_approved_amount = amount
        business_obj.save()
    return redirect('registered_businesses')
# def authorisedperson_detail(request):
#     business_id = request.session['business_id']
#     if request.method == "POST":
#         name = request.POST.get('name_authorised_person')
#         location = request.POST.get('location')
#         designation = request.POST.get('designation')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         mobile = request.POST.get('mobile')
#         business_obj = Business.objects.get(business_id=business_id)
#         obj = AuthorisedPerson_details.objects.create(name=name, location=location, designation=designation, email=email, phone=phone, mobile=mobile,business_id=business_obj)
#
#     return redirect('business_detail', business_id)

def invard_cheque(request):
    business_id = request.session['business_id']
    print(business_id)
    if request.method == "POST":
        bank_account_no = request.POST.get('accno')
        print(bank_account_no)
        number_of_instances = request.POST.get('number_of_instances')
        print(number_of_instances)
        amount = request.POST.get('amount')
        print(amount)
        business_obj = Business.objects.get(business_id=business_id)
        InvardchequeReturns.objects.create(bank_account_no=bank_account_no,number_of_instances=number_of_instances,amount=amount,business_id=business_obj)

    return redirect('bank_detail')

def debit_credit(request):
    business_id = request.session['business_id']
    print("debit_credit", business_id)
    if request.method == "POST":
        bank_account_no = request.POST.get('accno')
        number_of_party = request.POST.get('name_of_party')
        total_credit = request.POST.get('total_credit')
        total_debit = request.POST.get('total_debit')
        business_obj = Business.objects.get(business_id=business_id)
        Debit_credit_same_party.objects.create(bank_account_no=bank_account_no,number_of_party=number_of_party,total_credit=total_credit, total_debit=total_debit,business_id=business_obj)
    return redirect('bank_detail')
def loan_detail(request):
    business_id = request.session['business_id']
    if request.method == "POST":
        bank_account_no = request.POST.get('accno')
        amount_of_loan = request.POST.get('amount')
        date_of_transaction = request.POST.get('date')
        name_of_the_lender = request.POST.get('lender_name')
        business_obj = Business.objects.get(business_id=business_id)
        Loan_details_in_last_tweleve_months.objects.create(bank_account_no=bank_account_no, amount_of_loan=amount_of_loan, date_of_transaction=date_of_transaction, name_of_the_lender=name_of_the_lender, business_id=business_obj)
    return redirect('bank_detail')
def business_info(request):
    return redirect('bank_detail')
def emi_payement(request):
    business_id = request.session['business_id']
    if request.method == "POST":
        bank_account_no = request.POST.get('accno')
        emi_amount = request.POST.get('emi_amount')
        date_of_transaction = request.POST.get('transaction_date')
        business_obj = Business.objects.get(business_id=business_id)
        EMI_payement_details.objects.create(bank_account_no=bank_account_no,emi_amount=emi_amount, date_of_transaction=date_of_transaction,business_id=business_obj)
    return redirect('bank_detail')
def top_credits(request):
    business_id = request.session['business_id']
    if request.method == "POST":
        bank_account_no = request.POST.get('accno')
        entity_name = request.POST.get('name_of_party')
        emi_amount = request.POST.get('amount')
        date = request.POST.get('date')
        business_obj = Business.objects.get(business_id=business_id)
        Top_ten_credits.objects.create(bank_account_no=bank_account_no, entity_name=entity_name, emi_amount=emi_amount, date=date,business_id=business_obj)
    return redirect('bank_detail')

def top_debits(request):
    business_id = request.session['business_id']
    if request.method == "POST":
        bank_account_no = request.POST.get('accno')
        entity_name = request.POST.get('name_of_party')
        emi_amount = request.POST.get('amount')
        date = request.POST.get('date')
        business_obj = Business.objects.get(business_id=business_id)
        Top_ten_debits.objects.create(bank_account_no=bank_account_no,entity_name=entity_name,emi_amount=emi_amount, date=date, business_id=business_obj)
    return redirect('bank_detail')

def gstr_one(request):
    gst_num = request.session['gst_number']
    if request.method == "POST":
        domestic_sale = request.POST.get('domestic-sale')
        print(domestic_sale)
        # gst_num = request.session['gst_num']
        print(gst_num)
        export_sale = request.POST.get('export-sale')
        print(export_sale)
        obj= GSTDetails_new.objects.get(gst_No=gst_num)
        print(obj)
        obj.domestic_sale = domestic_sale
        obj.domestic_sale = domestic_sale
        obj.save()
        # for i in objs:
        #     print(i)
        #     i.domestic_sale = domestic_sale
        #     i.export_sale = export_sale
        #     i.save()
    return redirect('gst_detail')
def gstr_three(request):
    gst_num = request.session['gst_number']
    if request.method == "POST":
        sale_gast_three = request.POST.get('sale_gast_three')
        deviation_sale = request.POST.get('deviation_sale')
        obj = GSTDetails_new.objects.get(gst_No=gst_num)
        obj.sales_as_per_gstr_thee = sale_gast_three
        obj.deviation_from_sale = deviation_sale
        obj.save()
    print("gstr_three", gst_num)
    return redirect('gst_detail')
def gst_filter(request):
    if request.GET.get('gst_num'):
        gst_number = request.GET.get('gst_num')
        print("In gst number",gst_number)
        request.session['gst_number'] = gst_number
        gst_objs = GSTDetails_new.objects.get(gst_No=gst_number)
        print(gst_objs)
        domestic_sale = gst_objs.domestic_sale
        print(domestic_sale)
        export_sale = gst_objs.export_sale
        print(export_sale)
    return redirect('gst_detail')
    # domestic_sale_one  = domestic_sale
    # print(domestic_sale_one)
def gst_sale(request):
    gst_num = request.session['gst_number']
    print("In gst sale", gst_num)
    if request.method == "POST":
        name = request.POST.get('name')
        sale = request.POST.get('sale')
        GST_sale.objects.create(gst_no=gst_num, name=name, sale=sale)
    return redirect("gst_detail")

def gst_customer(request):
    gst_num = request.session['gst_number']
    print("In gst sale", gst_num)
    if request.method == "POST":
        name = request.POST.get('name')
        sale = request.POST.get('sale')
        GST_customers.objects.create(gst_no=gst_num, name=name, sale=sale)
    return redirect("gst_detail")

def gst_supplier(request):
    gst_num = request.session['gst_number']
    print("In gst sale", gst_num)
    if request.method == "POST":
        name = request.POST.get('name')
        purchase = request.POST.get('purchase')
        GST_suppliers.objects.create(gst_no=gst_num, name=name, purchase=purchase)
    return redirect("gst_detail")

def gst_product(request):
    gst_num = request.session['gst_number']
    print("In gst sale", gst_num)
    if request.method == "POST":
        product = request.POST.get('code_of_product')
        sale = request.POST.get('sale')
        GST_products.objects.create(gst_no=gst_num, code_of_product=product, sales=sale)
    return redirect('gst_detail')

def bankdetail_comment(request):
    print(request.user)
    business_id = request.session['business_id']
    print("bankdetail_comment",business_id)
    if request.method == "POST":
        comment = request.POST.get('comment')
        print(comment)
        type = request.POST.get('type')
        print(type)
        business_obj = Business.objects.get(business_id=business_id)
        request.session['type'] = type
        print(business_obj)
        Comments.objects.create(business_id=business_obj, username=request.user, comment=comment, type=type)
        if type == "bankdetail":
            return redirect('bank_detail')
        elif type == "gstdetail":
            return redirect('gst_detail')
        elif type == "customerdetail":
            return redirect('customer_detail')
        elif type == "supplierdetail":
            return redirect('supplier_detail')
        elif type == "financialdetail":
            return redirect('financial_detail')
        elif type == "businessdetail":
            return redirect('business_detail', business_id)
        elif type == "shareholdingdetail":
            return redirect('shareholding_detail')
        elif type == "debtprofiledetail":
            return redirect('debt_profile')
        elif type == "analysisreport":
            return redirect('analysis_report')
        elif type == "creditratingdetail":
            return redirect('credit_rating')
        elif type == "kycdetail":
            return redirect('KYC_detail')


    # return redirect('bank_detail')

def financial_calculations(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    ebidta = request.GET.get('ebidta')
    res = round((int(ebidta) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_ly=sales, ebitdta_ly=ebidta, ebidta_per_m_ly=res,
                                              business_id=business_obj)
    else:
        obj.sales_ly = sales
        obj.ebitdta_ly = ebidta
        obj.ebidta_per_m_ly = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_two(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    ebidta = request.GET.get('ebidta')
    res = round((int(ebidta) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)

    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_py=sales, ebitdta_py=ebidta, ebidta_per_m_py=res,
                                              business_id=business_obj)
    else:
        obj.sales_py = sales
        obj.ebitdta_py = ebidta
        obj.ebidta_per_m_py = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_three(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    ebidta = request.GET.get('ebidta')
    res = round((int(ebidta) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)

    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_cy=sales, ebitdta_cy=ebidta, ebidta_per_m_cy=res,
                                              business_id=business_obj)
    else:
        obj.sales_cy = sales
        obj.ebitdta_cy = ebidta
        obj.ebidta_per_m_cy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_four(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    ebidta = request.GET.get('ebidta')
    res = round((int(ebidta) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)

    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_lqy=sales, ebitdta_lqy=ebidta, ebidta_per_m_lqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_lqy = sales
        obj.ebitdta_lqy = ebidta
        obj.ebidta_per_m_lqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_five(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    ebidta = request.GET.get('ebidta')
    res = round((int(ebidta) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)

    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_sqy=sales, ebitdta_sqy=ebidta, ebidta_per_m_sqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_sqy = sales
        obj.ebitdta_sqy = ebidta
        obj.ebidta_per_m_sqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_six(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pat = request.GET.get('pat')
    res = round((int(pat) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_ly=sales, pat_ly=pat, pat_per_ly=res,
                                              business_id=business_obj)
    else:
        obj.sales_ly = sales
        obj.pat_ly = pat
        obj.pat_per_ly = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)
def financial_calculations_seven(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pat = request.GET.get('pat')
    res = round((int(pat) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_py=sales, pat_py=pat, pat_per_py=res,
                                              business_id=business_obj)
    else:
        obj.sales_py = sales
        obj.pat_py = pat
        obj.pat_per_py = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_eight(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pat = request.GET.get('pat')
    res = round((int(pat) / int(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_py=sales, pat_py=pat, pat_per_py=res,
                                              business_id=business_obj)
    else:
        obj.sales_py = sales
        obj.pat_py = pat
        obj.pat_per_py = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def bank_statement(request):
    return render(request, 'InvestorDashboards/bankstatement.html')


def company_details(request):
    return render(request, 'InvestorDashboards/companydetails.html')


def gst_details(request):
    return render(request, 'InvestorDashboards/gstdetails.html')


def pan_details(request):
    return render(request, 'InvestorDashboards/pandetails.html')

def details(request):
    x = Business.objects.all()
    print(x)
    return render(request, 'InvestorDashboards/test.html', {'x': x})

def test1(request, pk):
    a = get_object_or_404(BusinessDetails_test, pk=pk)
    print(a)
    return request(request, 'InvestorDashboards/test1.html')
