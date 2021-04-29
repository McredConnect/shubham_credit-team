from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from Investors.models import *
from tests.models import *
from django.template.loader import render_to_string, get_template
from .forms import *


def bank_detail(request):
    business_id = request.session['business_id']
    print("In bank detail", business_id)
    objs = BankstatementDetails_new.objects.filter(business_id=business_id)
    inverd_cheque = InvardchequeReturns.objects.filter(business_id=business_id)
    debit_credit_objs = Debit_credit_same_party.objects.filter(business_id=business_id)
    loan_detail_obj = Loan_details_in_last_tweleve_months.objects.filter(business_id=business_id)
    emi_obj = EMI_payement_details.objects.filter(business_id=business_id)
    credit_obj = Top_ten_credits.objects.filter(business_id=business_id)
    debits_obj = Top_ten_debits.objects.filter(business_id=business_id)
    comments_obj = Comments.objects.filter(type="bankdetail") & Comments.objects.filter(business_id=business_id)
    print("comments_obj",comments_obj)
    print("in bankdetail", objs)
    context = {'objs': objs, 'business_id':business_id, 'inverd_cheque':inverd_cheque, 'debit_credit_objs':debit_credit_objs, 'loan_detail_obj':loan_detail_obj, 'emi_obj':emi_obj, 'credit_obj':credit_obj, 'debits_obj':debits_obj,'comments_obj':comments_obj,'company':"company"}
    if request.method == "POST":
        bankname = request.POST.get('bankname')
        acctype = request.POST.get('acctype')
        accno = request.POST.get('accno')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        file = request.FILES['file1']
        business_obj = Business.objects.get(business_id=business_id)
        obj = BankstatementDetails_new.objects.create(bank_name=bankname, AC_No=accno, AC_Type=acctype,
                                                           from_date=fromdate, To_date=todate, input_file=file,business_id=business_obj)
        if obj:
            return redirect('bank_detail')
    return render(request, 'InvestorDashboards/test1.html', context)

def debt_profile(request):
    business_id = request.session['business_id']
    comments_obj = Comments.objects.filter(type="debtprofiledetail") & Comments.objects.filter(business_id=business_id)
    objs = DebtProfile_new.objects.filter(business_id=business_id)
    for i in objs:
        print(i.input_file)
    print("debt profile",business_id)
    context = {'objs': objs, 'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        name_of_lender = request.POST.get('nameoflender')
        type_of_loan = request.POST.get('typeofloan')
        amount_of_loan = request.POST.get('amountofloan')
        outstanding_amount = request.POST.get('outstandingamount')
        rate_of_interest = request.POST.get('rateofinterest')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = DebtProfile_new.objects.create(name_of_lender = name_of_lender,type_of_loan = type_of_loan, amount_of_loan=amount_of_loan,outstanding_amount = outstanding_amount, rate_of_interest = rate_of_interest, input_file=input_file,business_id=business_obj)
        if obj:
            return redirect('debt_profile')
    return render(request, 'InvestorDashboards/debt_profile.html', context)

def credit_rating(request):
    business_id = request.session['business_id']
    print("In bank detail", business_id)
    objs = CreditRating_test.objects.filter(business_id=business_id)
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
        obj = CreditRating_test.objects.create(ratingagency = ratingagency, rating = rating, date_of_rating =  date_of_rating, amount_of_rating = amount_of_rating, input_file = input_file,business_id=business_obj)
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
    pan = business_obj.business_pan_card
    # gst_num_obj = GSTDetails_test_new.objects.get(gst_No=gst_number)
    # domestic_sale = gst_num_obj.domestic_sale
    domestic_sale = 0
    # print(domestic_sale)
    # export_sale = gst_num_obj.export_sale
    export_sale = 0
    # print(export_sale)
    # sales_as_per_gstr_thee = gst_num_obj.sales_as_per_gstr_thee
    sales_as_per_gstr_thee = 0
    # deviation_from_sale = gst_num_obj.deviation_from_sale
    deviation_from_sale = 0

    # print(gst_num_obj)
    gst_sale_obj = GST_sale.objects.filter(gst_no=gst_number)
    gst_customer_obj = GST_customers.objects.filter(gst_no=gst_number)
    gst_suppliers_obj = GST_suppliers.objects.filter(gst_no=gst_number)
    gst_products_obj = GST_products.objects.filter(gst_no=gst_number)
    comments_obj = Comments.objects.filter(type="gstdetail") & Comments.objects.filter(business_id=business_id)
    print("In gst comments",comments_obj)
    gst_num = []
    gst_certificate = GSTDetails_test_new.objects.filter(gst_type="certificate") & GSTDetails_test_new.objects.filter(business_id=business_id)
    print(gst_certificate)
    objs = GSTDetails_test_new.objects.filter(business_id=business_id).exclude(gst_type="certificate")
    objs1 = GSTDetails_test_new.objects.filter(business_id=business_id)
    print("here with", objs)
    for i in objs1:
        val = i.gst_No
        gst_num.append(val)
    print("In gst details gst Num", gst_num)
    print("in gstdetail", objs)
    context = {'objs': objs,'business_id':business_id,'gst_num':set(gst_num),'domestic_sale':domestic_sale,'export_sale':export_sale,'sales_as_per_gstr_thee':sales_as_per_gstr_thee,'deviation_from_sale':deviation_from_sale,'gst_sale_obj':gst_sale_obj,'gst_customer_obj':gst_customer_obj,'gst_suppliers_obj': gst_suppliers_obj,'gst_products_obj':gst_products_obj,'comments_obj':comments_obj,'gst_certificate':gst_certificate}
    if request.method == "POST":
        gsttype = request.POST.get('gsttype')
        gstno = request.POST.get('gstnum')
        state = request.POST.get('state')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = GSTDetails_test_new.objects.create(gst_type=gsttype, gst_No=gstno, state=state,
                                                           fromdate=fromdate, Todate=todate, input_file=file,business_id=business_obj)
        if obj:
            return redirect('gst_detail')
    return render(request, 'InvestorDashboards/gstdetail.html',context)

def about_company(request):
    print("IN about company")
    business_id = request.session['business_id']
    if request.method == "POST":
        yoi = request.POST.get('yoi')
        print(yoi)
        plant_location = request.POST.get('plant_location')
        print(plant_location)
        business_id = request.session['business_id']
        print(business_id)
        business_obj = Business.objects.get(business_id=business_id)
        business_obj.year_of_incorporation = yoi
        business_obj.plant_location = plant_location
        business_obj.save()
    return redirect('business_detail',business_id)


def financial_detail(request):
    business_id = request.session['business_id']
    print("In financial detail", business_id)
    objs = Financialdetail_test.objects.filter(business_id=business_id)
    try:
        financial_calculations_obj = Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        financial_calculations_obj = []
    # financial_calculations_obj = Financial_calculations.objects.get(business_id=business_id)
    print(financial_calculations_obj)
    comments_obj = Comments.objects.filter(type="financialdetail") & Comments.objects.filter(business_id=business_id)
    print("in financialdetail", objs)
    context = {'objs': objs,'business_id':business_id, 'comments_obj':comments_obj, 'financial_calculations_obj':financial_calculations_obj}
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
    business_obj = Business.objects.get(business_id=business_id)
    yoi = business_obj.year_of_incorporation
    pl = business_obj.plant_location
    company = business_obj.user_id.organisation
    print(company)
    location = business_obj.city
    address = business_obj.business_address
    print(address)
    add = ""
    lst1 = []
    lst2 = []
    for i in range(2,len(address)-1):
        if address[i] == ",":
            lst1.append(address[i])
        elif address[i] == "'":
            lst1.append(address[i])
        else:
            lst2.append(address[i])
    print(lst1)
    print(lst2)
    for i in lst2:
        add = add + i
    add1 = add.split(" ")
    objs = BusinessDetails_test_new.objects.filter(business_id=pk)
    print(objs)
    authorisedperson_obj = AuthorisedPerson_details_new.objects.filter(business_id=business_id)
    # {{objs.business_id.user_id.username}}
    print(authorisedperson_obj)
    comments_obj = Comments.objects.filter(type="businessdetail") & Comments.objects.filter(business_id=business_id)
    if len(objs)>0:
        for i in objs:
            # company = i.business_id.user_id.username
            # company = "company name"
            # 'company': company,
            sector = i.business_id.sector
    else:
        sector = ""
    context = {'objs': objs, 'pl':pl,'yi':yoi,'sector': sector, 'business_id': business_id, 'company': company, 'authorisedperson_obj':authorisedperson_obj,'comments_obj': comments_obj,'location': location,'add': add}
    if request.method == "POST":
        file_type = request.POST.get('filetype')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=pk)
        obj = BusinessDetails_test_new.objects.create(file_name=file_type, username=request.user, input_file=input_file, business_id=business_obj)
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
    if len(objs)>0:
        for i in objs:
            average_monthly_sale = i.average_monthly_sale
            print(average_monthly_sale)
            total_annual_sale = i.total_annual_sale
    comments_obj = Comments.objects.filter(type="customerdetail") & Comments.objects.filter(business_id=business_id)
    approved_customer_obj = Approvedcustomers.objects.filter(business_id=business_id)
    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj, 'approved_customer_obj':approved_customer_obj}
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

def director_list(request):
    business_id = request.session['business_id']
    print("In KYCdetail detail", business_id)
    objs = Director_list.objects.filter(business_id=business_id)
    print("in KYCdetail", objs)
    comments_obj = Comments.objects.filter(type="directorlist") & Comments.objects.filter(business_id=business_id)
    context = {'objs':objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        name_of_the_director = request.POST.get('name')
        address = request.POST['address']
        DIN_number = request.POST.get('din_no')
        Aadhar_number = request.POST.get('aadhar_no')
        Aadhar_file = request.FILES['file1']
        Pan_number = request.POST.get('pan_no')
        input_file = request.FILES['file2']
        business_obj = Business.objects.get(business_id=business_id)
        obj = Director_list.objects.create(name_of_the_director=name_of_the_director, address=address,Aadhar_number=Aadhar_number,Aadhar_file=Aadhar_file, DIN_number=DIN_number,Pan_number=Pan_number, input_file=input_file, business_id=business_obj)
        if obj:
            return redirect('director_list')
    return render(request, 'InvestorDashboards/list_of_directors.html',context)
def approved_customer_detail(request):
    business_id = request.session['business_id']
    # print("In customer_detail detail", business_id)
    # objs = Approvedcustomers.objects.filter(business_id=business_id)
    # print("in customer_detail", objs)
    # comments_obj = Comments.objects.filter(type="customerdetail") & Comments.objects.filter(business_id=business_id)
    #
    # context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        name_of_customer = request.POST.get('name')
        last_tweleve_month_sale = request.POST.get('sale')
        sale_as_per_gst = request.POST.get('sale_gst')
        business_obj = Business.objects.get(business_id=business_id)
        Approvedcustomers.objects.create(name_of_customer=name_of_customer, last_tweleve_month_sale=last_tweleve_month_sale, sale_as_per_gst=sale_as_per_gst, business_id=business_obj)
    return redirect('customer_detail')

def supplier_detail(request):
    business_id = request.session['business_id']
    print("In customer_detail detail", business_id)
    objs = Suppliersdetails_new.objects.filter(business_id=business_id)
    print("in customer_detail", objs)
    approved_supplier_obj = Approvedsuppliers.objects.filter(business_id=business_id)
    comments_obj = Comments.objects.filter(type="supplierdetail") & Comments.objects.filter(business_id=business_id)
    context = {'objs': objs, 'business_id':business_id, 'comments_obj':comments_obj, 'approved_supplier_obj':approved_supplier_obj}
    if request.method == "POST":
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
        obj = Suppliersdetails_new.objects.create(name=name, purchase=purchase, last_tweleve_month_sale=last_tweleve_month_sale, fromdate=fromdate,
                                              todate=todate, input_file=input_file,business_id=business_obj)
        print(obj)
        if obj:
            return redirect('supplier_detail')
    return render(request, 'InvestorDashboards/suppliers.html', context)

def approved_supplier_detail(request):
    business_id = request.session['business_id']
    # print("In customer_detail detail", business_id)
    # objs = Approvedcustomers.objects.filter(business_id=business_id)
    # print("in customer_detail", objs)
    # comments_obj = Comments.objects.filter(type="customerdetail") & Comments.objects.filter(business_id=business_id)
    #
    # context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        name_of_customer = request.POST.get('name')
        last_tweleve_month_purchase = request.POST.get('sale')
        purchase_as_per_gst = request.POST.get('purchase_gst')
        business_obj = Business.objects.get(business_id=business_id)
        Approvedsuppliers.objects.create(name_of_customer=name_of_customer, last_tweleve_month_purchase=last_tweleve_month_purchase, purchase_as_per_gst=purchase_as_per_gst, business_id=business_obj)
    return redirect('supplier_detail')


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
    objs = KYCdetail_new.objects.filter(business_id=business_id)
    print("in KYCdetail", objs)
    comments_obj = Comments.objects.filter(type="kycdetail") & Comments.objects.filter(business_id=business_id)
    context = {'objs': objs,'business_id':business_id,'comments_obj':comments_obj}
    if request.method == "POST":
        Name_of_directors = request.POST.get('name')
        Type_of_ID = request.POST['typeofid']
        ID_NO = request.POST.get('ID_NO')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = KYCdetail_new.objects.create(Name_of_directors=Name_of_directors, Type_of_ID=Type_of_ID, ID_NO=ID_NO, input_file=input_file, business_id=business_obj)
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
        obj = AuthorisedPerson_details_new.objects.create(name=name, location=location, designation=designation, email=email, phone=phone, mobile=mobile,business_id=business_obj)

    return redirect('business_detail', business_id)

def AS26_detail(request):
    business_id = request.session['business_id']
    # print("In KYCdetail detail", business_id)
    objs = As26detail.objects.filter(business_id=business_id)
    # print("in KYCdetail", objs)
    context = {'objs': objs,'business_id':business_id}
    if request.method == "POST":
        name_of_document = request.POST.get('reportname')
        fromdate = request.POST['fromdate']
        todate = request.POST.get('todate')
        input_file = request.FILES['file']
        business_obj = Business.objects.get(business_id=business_id)
        obj = As26detail.objects.create(name_of_document=name_of_document, fromdate=fromdate, todate=todate, input_file=input_file, business_id=business_obj)
        if obj:
            return redirect('AS26_detail')
    return render(request, 'InvestorDashboards/bankdetail.html', context)


def removeobj(request, pk):
    business_id = request.session['business_id']
    print("business_id=", business_id)
    print(pk)
    BusinessDetails_test_obj = BusinessDetails_test_new.objects.filter(id=pk).first()
    if BusinessDetails_test_obj:
        BusinessDetails_test_obj.delete()
    return redirect('business_detail', business_id)

def removeobj_bankdetail(request, pk):
    BankstatementDetails_test_obj = BankstatementDetails_new.objects.filter(id=pk).first()
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
    GSTDetails_test_obj = GSTDetails_test_new.objects.filter(id=pk).first()
    if GSTDetails_test_obj:
        GSTDetails_test_obj.delete()
    return redirect('gst_detail')

def remove_authorisedperson(request, pk):
    business_id = request.session['business_id']
    AuthorisedPerson_details_obj = AuthorisedPerson_details_new.objects.filter(id=pk).first()
    if AuthorisedPerson_details_obj:
        AuthorisedPerson_details_obj.delete()
    return redirect('business_detail', business_id)

def remove_debt_profile(request, pk):
    DebtProfile_obj = DebtProfile_new.objects.filter(id=pk).first()
    if DebtProfile_obj:
        DebtProfile_obj.delete()
    return redirect('debt_profile')

def remove_analysisreport(request, pk):
    Analysisreports_obj = Analysisreports.objects.filter(id=pk).first()
    if Analysisreports_obj:
        Analysisreports_obj.delete()
    return redirect('analysis_report')

def remove_creditrating(request, pk):
    CreditRating_obj = CreditRating_test.objects.filter(id=pk).first()
    if CreditRating_obj:
        CreditRating_obj.delete()
    return redirect('credit_rating')

def remove_KYCdetail(request, pk):
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
    Suppliersdetails_obj = Suppliersdetails_new.objects.filter(id=pk).first()
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
    objs = Business.objects.filter(status="New").order_by('-created_date')
    print(objs)
    context = {'objs':objs}
    return render(request, 'InvestorDashboards/business.html', context)


def investor(request):
    print("In investor view")
    objs = Investor.objects.filter(status="New")
    print(objs)
    context = {'objs':objs}
    return render(request, 'InvestorDashboards/investors.html', context)

def investor_detail(request,pk):
    context = {'pk':pk}
    investor_obj = Investor.objects.get(investor_id=pk)
    type = investor_obj.investor_category
    print(type)
    if type == "Individual":
        return redirect('Individual', pk)
    if type == "Private Limited":
        return redirect('privatelimited',pk)
    if type == "HUF":
        return redirect('huf', pk)
    if type == "Partnership":
        return redirect('Partnership', pk)
    if type == "NBFC / Bank":
        return redirect('Nbfc', pk)
    if type == "NRI":
        return redirect('Nri', pk)
    if type == "Partnership / LLP":
        return redirect('Partnership_LLP', pk)
    return render(request, 'InvestorDashboards/investor_detail.html', context)

def privatelimited(request, pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    context = {'pk':pk,'investor_obj':investor_obj}
    if request.method == "POST":
        entity_name = request.POST.get('entity_name')
        entity_type = request.POST.get('entity_type')
        entity_pan_num = request.POST.get('entity_pan_num')
        authoriseduser_name = request.POST.get('authoriseduser_name')
        authoriseduser_mobile_num = request.POST.get('authoriseduser_mobile_num')
        authoriseduser_email = request.POST.get('authoriseduser_email')
        authoriseduser_pan_num = request.POST.get('authoriseduser_pan_num')
        authoriseduser_aadhar_num = request.POST.get('authoriseduser_aadhar_num')
        print(investor_obj)
        investor_obj.investor_name = entity_name
        investor_obj.investor_category = entity_type
        investor_obj.investor_PAN = entity_pan_num
        investor_obj.investor_authorised_user_name = authoriseduser_name
        investor_obj.investor_authorised_user_mobile = authoriseduser_mobile_num
        investor_obj.investor_authorised_user_email = authoriseduser_email
        investor_obj.investor_authorised_user_PAN = authoriseduser_pan_num
        investor_obj.investor_authorised_user_Aadhaar = authoriseduser_aadhar_num
        investor_obj.save()
        return redirect('privatelimited',pk)
    return render(request, 'InvestorDashboards/privatelimited.html', context)

def privatelimited_file(request,pk):
    if request.method == "POST":
        entity_date = request.POST.get('entity_date')
        authorised_date = request.POST.get('authorised_date')
        entity_pan_photo = request.FILES['entity_pan_photo']
        entity_coi = request.FILES['entity_coi']
        entity_rp = request.FILES['entity_rp']
        authorised_pan_photo = request.FILES['authorised_pan_photo']
        authorised_aadhar_photo = request.FILES['authorised_aadhar_photo']
        investor_obj = Investor.objects.get(investor_id=pk)
        print('nbfc file',investor_obj)
        investor_obj.investor_date_of_incorporation = entity_date
        investor_obj.investor_authorised_user_DOB = authorised_date
        investor_obj.investor_PAN_proof = entity_pan_photo
        investor_obj.investor_cert_incorporation = entity_coi
        investor_obj.investor_resolution = entity_rp
        investor_obj.investor_authorised_user_PAN_proof = authorised_pan_photo
        investor_obj.investor_authorised_user_Aadhaar_proof = authorised_aadhar_photo
        investor_obj.save()
        return redirect('privatelimited',pk)


def huf(request, pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    context = {'investor_obj':investor_obj,'pk':pk}
    if request.method == "POST":
        entity_name = request.POST.get('entity_name')
        entity_type = request.POST.get('entity_type')
        entity_pan_num = request.POST.get('entity_pan_num')
        authoriseduser_name = request.POST.get('authoriseduser_name')
        authoriseduser_mobile_num = request.POST.get('authoriseduser_mobile_num')
        authoriseduser_email = request.POST.get('authoriseduser_email')
        authoriseduser_pan_num = request.POST.get('authoriseduser_pan_num')
        authoriseduser_aadhar_num = request.POST.get('authoriseduser_aadhar_num')
        print(investor_obj)
        investor_obj.investor_name = entity_name
        investor_obj.investor_category = entity_type
        investor_obj.investor_PAN = entity_pan_num
        investor_obj.investor_authorised_user_name = authoriseduser_name
        investor_obj.investor_authorised_user_mobile = authoriseduser_mobile_num
        investor_obj.investor_authorised_user_email = authoriseduser_email
        investor_obj.investor_authorised_user_PAN = authoriseduser_pan_num
        investor_obj.investor_authorised_user_Aadhaar = authoriseduser_aadhar_num
        investor_obj.save()
        return redirect('huf',pk)
    return render(request, 'InvestorDashboards/huf.html', context)

def huf_file(request,pk):
    if request.method == "POST":
        entity_date = request.POST.get('entity_date')
        authorised_date = request.POST.get('authorised_date')
        entity_pan_photo = request.FILES['entity_pan_photo']
        authorised_pan_photo = request.FILES['authorised_pan_photo']
        authorised_aadhar_photo = request.FILES['authorised_aadhar_photo']
        investor_obj = Investor.objects.get(investor_id=pk)
        print('nbfc file',investor_obj)
        investor_obj.investor_date_of_incorporation = entity_date
        investor_obj.investor_authorised_user_DOB = authorised_date
        investor_obj.investor_PAN_proof = entity_pan_photo

        investor_obj.investor_authorised_user_PAN_proof = authorised_pan_photo
        investor_obj.investor_authorised_user_Aadhaar_proof = authorised_aadhar_photo
        investor_obj.save()
        return redirect('huf',pk)

def Partnership(request, pk):
    context = {'pk':pk}
    return render(request, 'InvestorDashboards/Partnership.html', context)

def Nbfc(request, pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    context = {'investor_obj':investor_obj,'pk':pk}
    if request.method == "POST":
        entity_name = request.POST.get('entity_name')
        entity_type = request.POST.get('entity_type')
        entity_pan_num = request.POST.get('entity_pan_num')
        authoriseduser_name = request.POST.get('authoriseduser_name')
        authoriseduser_mobile_num = request.POST.get('authoriseduser_mobile_num')
        authoriseduser_email = request.POST.get('authoriseduser_email')
        authoriseduser_pan_num = request.POST.get('authoriseduser_pan_num')
        authoriseduser_aadhar_num = request.POST.get('authoriseduser_aadhar_num')
        print(investor_obj)
        investor_obj.investor_name = entity_name
        investor_obj.investor_category = entity_type
        investor_obj.investor_PAN = entity_pan_num
        investor_obj.investor_authorised_user_name = authoriseduser_name
        investor_obj.investor_authorised_user_mobile = authoriseduser_mobile_num
        investor_obj.investor_authorised_user_email = authoriseduser_email
        investor_obj.investor_authorised_user_PAN = authoriseduser_pan_num
        investor_obj.investor_authorised_user_Aadhaar = authoriseduser_aadhar_num
        investor_obj.save()
        return redirect('Nbfc',pk)
    return render(request, 'InvestorDashboards/Nbfc.html', context)

def nbfc_file(request,pk):
    if request.method == "POST":
        entity_date = request.POST.get('entity_date')
        authorised_date = request.POST.get('authorised_date')
        entity_pan_photo = request.FILES['entity_pan_photo']
        entity_coi = request.FILES['entity_coi']
        entity_rp = request.FILES['entity_rp']
        authorised_pan_photo = request.FILES['authorised_pan_photo']
        authorised_aadhar_photo = request.FILES['authorised_aadhar_photo']
        investor_obj = Investor.objects.get(investor_id=pk)
        print('nbfc file',investor_obj)
        investor_obj.investor_date_of_incorporation = entity_date
        investor_obj.investor_authorised_user_DOB = authorised_date
        investor_obj.investor_PAN_proof = entity_pan_photo
        investor_obj.investor_cert_incorporation = entity_coi
        investor_obj.investor_resolution = entity_rp
        investor_obj.investor_authorised_user_PAN_proof = authorised_pan_photo
        investor_obj.investor_authorised_user_Aadhaar_proof = authorised_aadhar_photo
        investor_obj.save()
        return redirect('Nbfc',pk)

def Nri(request,pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    context = {'pk':pk,'investor_obj':investor_obj}
    if request.method == "POST":
        name = request.POST.get('name')
        type = request.POST.get('type')
        mobile_num = request.POST.get('mobile_num')
        email = request.POST.get('email')
        pan_num = request.POST.get('pan_num')
        gst_num = request.POST.get('gst_num')
        print("In indivisual post",name)
        print(investor_obj)
        investor_obj.investor_name = name
        investor_obj.investor_category = type
        investor_obj.contact_no = mobile_num
        investor_obj.investor_email = email
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_gs_number = gst_num
        investor_obj.save()
        return redirect('Nri',pk)
    return render(request, 'InvestorDashboards/Nri.html', context)

def Nri_file(request,pk):
    if request.method == "POST":
        date = request.POST.get('date')
        print('in indivisual file',date)
        pan_photo = request.FILES['pan_photo']
        print(pan_photo)
        aadhar_photo = request.FILES['aadhar_photo']
        print(aadhar_photo)
        nri_proof = request.FILES['nri_proof']
        gst_proof = request.FILES['gst_proof']
        investor_obj = Investor.objects.get(investor_id=pk)
        print('indivisual file',investor_obj)
        investor_obj.investor_date_of_incorporation = date
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_Aadhaar_proof = aadhar_photo
        investor_obj.investor_NRI_proof = nri_proof
        investor_obj.investor_gst_proof = gst_proof
        investor_obj.save()
        return redirect('Nri',pk)

def Individual(request,pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    context = {'investor_obj':investor_obj,'pk':pk}
    if request.method == "POST":
        name = request.POST.get('name')
        type = request.POST.get('type')
        mobile_num = request.POST.get('mobile_num')
        email = request.POST.get('email')
        pan_num = request.POST.get('pan_num')
        aadhar_num = request.POST.get('aadhar_num')
        gst_num = request.POST.get('gst_num')
        print("In indivisual post",name)
        print(investor_obj)
        investor_obj.investor_name = name
        investor_obj.investor_category = type
        investor_obj.contact_no = mobile_num
        investor_obj.investor_email = email
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_Aadhaar = aadhar_num
        investor_obj.investor_gs_number = gst_num
        investor_obj.save()
        return redirect('Individual',pk)

    return render(request, 'InvestorDashboards/investor_detail.html', context)

def indivisual_file(request,pk):
    print("In indivisual file")
    if request.method == "POST":
        date = request.POST.get('date')
        print('in indivisual file',date)
        pan_photo = request.FILES['pan_photo']
        print(pan_photo)
        aadhar_photo = request.FILES['aadhar_photo']
        print(aadhar_photo)
        gst_proof = request.FILES['gst_proof']
        print(gst_proof)
        investor_obj = Investor.objects.get(investor_id=pk)
        print('indivisual file',investor_obj)
        investor_obj.investor_date_of_incorporation = date
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_Aadhaar_proof = aadhar_photo
        investor_obj.investor_gst_proof = gst_proof
        investor_obj.save()
        return redirect('Individual',pk)

def Partnership_LLP(request,pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    context = {'investor_obj':investor_obj,'pk':pk}
    if request.method == "POST":
        entity_name = request.POST.get('entity_name')
        entity_type = request.POST.get('entity_type')
        entity_pan_num = request.POST.get('entity_pan_num')
        authoriseduser_name = request.POST.get('authoriseduser_name')
        authoriseduser_mobile_num = request.POST.get('authoriseduser_mobile_num')
        authoriseduser_email = request.POST.get('authoriseduser_email')
        authoriseduser_pan_num = request.POST.get('authoriseduser_pan_num')
        authoriseduser_aadhar_num = request.POST.get('authoriseduser_aadhar_num')
        print(investor_obj)
        investor_obj.investor_name = entity_name
        investor_obj.investor_category = entity_type
        investor_obj.investor_PAN = entity_pan_num
        investor_obj.investor_authorised_user_name = authoriseduser_name
        investor_obj.investor_authorised_user_mobile = authoriseduser_mobile_num
        investor_obj.investor_authorised_user_email = authoriseduser_email
        investor_obj.investor_authorised_user_PAN = authoriseduser_pan_num
        investor_obj.investor_authorised_user_Aadhaar = authoriseduser_aadhar_num
        investor_obj.save()
        return redirect('Partnership_LLP',pk)
    return render(request, 'InvestorDashboards/Partnership_LLP.html', context)


def Partnership_LLP_file(request,pk):
    if request.method == "POST":
        entity_date = request.POST.get('entity_date')
        authorised_date = request.POST.get('authorised_date')
        entity_pan_photo = request.FILES['entity_pan_photo']
        entity_coi = request.FILES['entity_coi']
        entity_rp = request.FILES['entity_rp']
        authorised_pan_photo = request.FILES['authorised_pan_photo']
        authorised_aadhar_photo = request.FILES['authorised_aadhar_photo']
        investor_obj = Investor.objects.get(investor_id=pk)
        print('nbfc file',investor_obj)
        investor_obj.investor_date_of_incorporation = entity_date
        investor_obj.investor_authorised_user_DOB = authorised_date
        investor_obj.investor_PAN_proof = entity_pan_photo
        investor_obj.investor_cert_incorporation = entity_coi
        investor_obj.investor_resolution = entity_rp
        investor_obj.investor_authorised_user_PAN_proof = authorised_pan_photo
        investor_obj.investor_authorised_user_Aadhaar_proof = authorised_aadhar_photo
        investor_obj.save()
        return redirect('Nbfc',pk)

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

def pending_investor(request):
    print("In business view")
    objs = Investor.objects.filter(status="PENDING")
    print(objs)
    context = {'objs': objs}
    return render(request, 'InvestorDashboards/pending_investor.html', context)

def approved_investor(request):
    print("In business view")
    objs = Investor.objects.filter(status="APPROVED")
    print(objs)
    context = {'objs': objs}
    return render(request, 'InvestorDashboards/approved_investor.html', context)

def pending_form(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/pendingform.html', context)

def approved_form(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/approvedform.html', context)

def investor_approved_form(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/investor_approvedform.html', context)

def approve_investor(request,pk):
    if request.method == "POST":
        investor_obj = Investor.objects.get(investor_id=pk)
        # investor_obj.status = "APPROVED"
        # investor_obj.save()
        return redirect('create-entity-investor')

    # return redirect('approved_investor')


def reason_form(request,pk):
    business_obj = Business.objects.get(business_id=pk)
    print(business_obj)
    # reason = business_obj.pending_reason
    business_reason_obj = Business_Reasons.objects.filter(business_id=business_obj)
    # print(reason)
    context = {'pk':pk,'reason':reason,'business_reason_obj':business_reason_obj}
    return render(request, 'InvestorDashboards/reasonform.html', context)

def investor_reason_form(request,pk):
    investor_obj = Investor.objects.get(investor_id=pk)
    investor_reason_obj = Investor_Reasons.objects.filter(investor_id=investor_obj) & Investor_Reasons.objects.filter(type="investor")
    print(investor_reason_obj)
    # reason = investor_obj.pending_reason
    context = {'pk':pk,'investor_reason_obj':investor_reason_obj}
    return render(request, 'InvestorDashboards/investorreasonform.html', context)

def business_comment(request, pk):
    # businessdetail_comments_obj = Comments.objects.filter(type="businessdetail") & Comments.objects.filter(business_id=business_id)
    comments_obj = Comments.objects.filter(business_id=pk)
    context = {'comments_obj': comments_obj}
    return render(request, 'InvestorDashboards/business_comment.html', context)
    # return render(request, 'InvestorDashboards/modal.html', context)


def business_comment_one(request):
    print('business_comment_one')
    id = request.GET.get('id')
    print(id)
    comments_obj = Comments.objects.filter(business_id=id)
    t = render_to_string('InvestorDashboards/business_comment.html', {'comments_obj':comments_obj})
    data = {'res':t}
    return JsonResponse(data)

def reason(request, pk):
    print("in REASON", pk)
    if request.method == "POST":
        message = request.POST.get('reason')
        print(message)
        business_obj = Business.objects.get(business_id=pk)
        print("BUSINESS OBJECTS IN REASON", business_obj)
        business_obj.status = "PENDING"
        business_obj.save()
        # business_obj.pending_reason = message
        # business_obj.save()
        Business_Reasons.objects.create(business_id=business_obj,reason=message)
    return redirect('pending_businesses')

def investor_reason(request, pk):
    print("IN INVESTOR  REASON", pk)
    if request.method == "POST":
        message = request.POST.get('reason')
        type = request.POST.get('type')
        print(type)
        print("in post message",message)
        investor_obj = Investor.objects.get(investor_id=pk)
        investor_obj.status = "PENDING"
        investor_obj.save()
        # investor_obj.pending_reason = message
        # investor_obj.save()
        # print("After post",investor_obj.pending_reason)
        Investor_Reasons.objects.create(investor_id=investor_obj,type=type,reason=message)
    return redirect('pending_investor')

def investor_reason_two(request,pk):
    if request.method == "POST":
        message = request.POST.get('reason')
        type = request.POST.get('type')
        print(type)
        print("in post message",message)
        investor_obj = Investor.objects.get(investor_id=pk)
        investor_obj.status = "PENDING"
        investor_obj.save()
        # investor_obj.pending_reason = message
        # investor_obj.save()
        # print("After post",investor_obj.pending_reason)
        Investor_Reasons.objects.create(investor_id=investor_obj,type=type,reason=message)
    return redirect('investor_reason_form',pk)
def fascilate_amount(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/fascilateamountform.html', context)

def enter_fascilate_amount(request, pk):
    context = {'pk': pk}
    return render(request, 'InvestorDashboards/fascilateamountform.html', context)

# TODO:
def fascilate_amount_save(request, pk):
    if request.method == "POST":
        amount = request.POST.get('amount')
        print(amount)
        business_obj = Business.objects.get(business_id=pk)
        print(business_obj)
        business_obj.facility_approved_amount = amount
        business_obj.available_facility_limit = amount
        business_obj.save()
    return redirect('create-entity-business')
    # return redirect('registered_businesses')

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

def snapshot(request):
    business_id = request.session['business_id']
    print(business_id)
    business_obj = Business.objects.get(business_id=business_id)
    comments_obj = Comments.objects.filter(type="snapshot") & Comments.objects.filter(business_id=business_id)
    if business_obj.sector:
        sector = business_obj.sector
    try:
        company = business_obj.user_id.username
    except:
        company = "company"
    # approved_customer_obj = Approvedcustomers.objects.filter(business_id=business_id)
    # shareholding_objs = Shareholding.objects.filter(business_id=business_id)
    # approved_supplier_obj = Approvedsuppliers.objects.filter(business_id=business_id)
    # credit_rating_objs = CreditRating_test.objects.filter(business_id=business_id)
    # business_profile_objs = BusinessProfile.objects.filter(business_id=business_id)
    # secured_loan = DebtProfile_new.objects.filter(type_of_loan="secured")
    # unsecured_loan = DebtProfile_new.objects.filter(type_of_loan="unsecured")
    # context = {'sector': sector, 'company': company, 'approved_customer_obj': approved_customer_obj,
    #  'shareholding_objs': shareholding_objs, 'approved_supplier_obj': approved_supplier_obj,
    #  'credit_rating_objs': credit_rating_objs, 'business_profile_objs': business_profile_objs,
    #  'comments_obj': comments_obj, 'secured_loan': secured_loan, 'unsecured_loan': unsecured_loan}
    return render(request, 'InvestorDashboards/snapshot.html',{'sector': sector, 'company': company})

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
        GSTR_one.objects.create(gst_no=gst_num,domestic_sale=domestic_sale,export_sale=export_sale)
    return redirect('gst_detail')

def gstr_three(request):
    gst_num = request.session['gst_number']
    if request.method == "POST":
        sale_gast_three = request.POST.get('sale_gast_three')
        deviation_sale = request.POST.get('deviation_sale')
        obj = GSTDetails_test_new.objects.get(gst_No=gst_num)
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
        gst_objs = GSTDetails_test_new.objects.filter(gst_No=gst_number)
        print(gst_objs)
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

def gst_certificate(request):
    business_id = request.session['business_id']
    print("In gst certificate")
    if request.method == "POST":
        gsttype = request.POST.get('type')
        print(gsttype)
        gstno = request.POST.get('gstnum')
        print(gstno)
        fromdate = request.POST.get('fromdate')
        print(fromdate)
        todate = request.POST.get('todate')
        print(todate)
        file = request.FILES['file']
        print(file)
        business_obj = Business.objects.get(business_id=business_id)
        GSTDetails_test_new.objects.create(gst_type=gsttype, gst_No=gstno,
                                                 fromdate=fromdate, Todate=todate, input_file=file,
                                                 business_id=business_obj)
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
        elif type == "snapshot":
            return redirect('snapshot')
        elif type == "as26detail":
            return redirect('snapshot')
        elif type == "directorlist":
            return redirect('director_list')


def financial_calculations(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    ebidta = request.GET.get('ebidta')
    res = round((float(ebidta) / float(sales)), 2)
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
    res = round((float(ebidta) / float(sales)), 2)
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
    res = round((float(ebidta) / float(sales)), 2)
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
    res = round((float(ebidta) / float(sales)), 2)
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
    res = round((float(ebidta) / float(sales)), 2)
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
    res = round((float(pat) / float(sales)), 2)
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
    res = round((float(pat) / float(sales)), 2)
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
    res = round((float(pat) / float(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_cy=sales, pat_cy=pat, pat_per_cy=res,
                                              business_id=business_obj)
    else:
        obj.sales_cy = sales
        obj.pat_cy = pat
        obj.pat_per_cy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_nine(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pat = request.GET.get('pat')
    res = round((float(pat) / float(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_lqy=sales, pat_lqy=pat, pat_per_lqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_lqy = sales
        obj.pat_lqy = pat
        obj.pat_per_lqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_ten(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pat = request.GET.get('pat')
    res = round((float(pat) / float(sales)), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_sqy=sales, pat_sqy=pat, pat_per_sqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_sqy = sales
        obj.pat_sqy = pat
        obj.pat_per_sqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_eleven(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pbt = request.GET.get('pbt')
    interest = request.GET.get('interest')
    res = round((float(interest) / float(sales)), 2)
    print(res)
    res1 = round((float(pbt) + float(interest)) / float(interest), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_ly=sales, pbt_ly=pbt, interest_ly=interest, interest_upon_sales_per_ly=res, int_coverage_ration_ly=res1,
                                              business_id=business_obj)
    else:
        obj.sales_ly = sales
        obj.pbt_ly = pbt
        obj.interest_ly = interest
        obj.interest_upon_sales_per_ly = res
        obj.int_coverage_ration_ly = res1
        obj.save()

    data = {'res': res,'res1': res1}
    return JsonResponse(data)

def financial_calculations_tweleve(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pbt = request.GET.get('pbt')
    interest = request.GET.get('interest')
    res = round((float(interest) / float(sales)), 2)
    print(res)
    res1 = round((float(pbt) + float(interest)) / float(interest), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_py=sales, pbt_py=pbt, interest_py=interest,interest_upon_sales_per_py=res,int_coverage_ration_py=res1,
                                              business_id=business_obj)
    else:
        obj.sales_py = sales
        obj.pbt_py = pbt
        obj.interest_py = interest
        obj.interest_upon_sales_per_py = res
        obj.int_coverage_ration_py = res1
        obj.save()
    data = {'res': res,'res1': res1}
    return JsonResponse(data)

def financial_calculations_thirteen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pbt = request.GET.get('pbt')
    interest = request.GET.get('interest')
    res = round((float(interest) / float(sales)), 2)
    print(res)
    res1 = round((float(pbt) + float(interest)) / float(interest), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_cy=sales, pbt_cy=pbt, interest_cy=interest,interest_upon_sales_per_cy=res,int_coverage_ration_cy=res1,
                                              business_id=business_obj)
    else:
        obj.sales_cy = sales
        obj.pbt_cy = pbt
        obj.interest_cy = interest
        obj.interest_upon_sales_per_cy = res
        obj.int_coverage_ration_cy = res1
        obj.save()
    data = {'res': res,'res1': res1}
    return JsonResponse(data)

def financial_calculations_fourteen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pbt = request.GET.get('pbt')
    interest = request.GET.get('interest')
    res = round((float(interest) / float(sales)), 2)
    print(res)
    res1 = round((float(pbt) + float(interest)) / float(interest), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_lqy=sales, pbt_lqy=pbt, interest_lqy=interest,interest_upon_sales_per_lqy=res,int_coverage_ration_lqy=res1,
                                              business_id=business_obj)
    else:
        obj.sales_lqy = sales
        obj.pbt_lqy = pbt
        obj.interest_lqy = interest
        obj.interest_upon_sales_per_lqy = res
        obj.int_coverage_ration_lqy = res1
        obj.save()

    data = {'res': res,'res1': res1}
    return JsonResponse(data)

def financial_calculations_fifteen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    pbt = request.GET.get('pbt')
    interest = request.GET.get('interest')
    res = round((float(interest) / float(sales)), 2)
    print(res)
    res1 = round((float(pbt) + float(interest)) / float(interest), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_sqy=sales, pbt_sqy=pbt, interest_sqy=interest,interest_upon_sales_per_sqy=res, int_coverage_ration_sqy=res1,
                                              business_id=business_obj)
    else:
        obj.sales_sqy = sales
        obj.pbt_sqy = pbt
        obj.interest_sqy = interest
        obj.interest_upon_sales_per_sqy = res
        obj.int_coverage_ration_sqy = res1
        obj.save()

    data = {'res': res, 'res1': res1}
    return JsonResponse(data)

def financial_calculations_sixteen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    networth = request.GET.get('networth')
    print(networth)
    print(type(networth))
    unsecured = request.GET.get('unsecured')
    secured = request.GET.get('secured')
    res = round((float(unsecured) / (float(unsecured)+float(secured))), 2)
    print(res)
    res1 = round((float(unsecured) + float(secured)) / float(networth), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(networth_ly=networth, unsecured_ly=unsecured, secured_ly=secured, percentage_of_unsecuredloan_upon_totalloan_one_ly=res,debt_upon_equity_one_ly=res1,
                                              business_id=business_obj)
    else:
        obj.networth_ly = networth
        obj.unsecured_ly = unsecured
        obj.secured_ly = secured
        obj.per_unsecured_upon_secured_ly = res
        obj.debt_upon_equity_ly = res1
        obj.save()

    data = {'res': res,'res1': res1}
    return JsonResponse(data)

def financial_calculations_seventeen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    networth = request.GET.get('networth')
    print(networth)
    print(type(networth))
    unsecured = request.GET.get('unsecured')
    secured = request.GET.get('secured')
    res = round((float(unsecured) / (float(unsecured)+float(secured))), 2)
    print(res)
    res1 = round((float(unsecured) + float(secured)) / float(networth), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(networth_py=networth, unsecured_py=unsecured, secured_py=secured, percentage_of_unsecuredloan_upon_totalloan_one_py=res, debt_upon_equity_one_py=res1,
                                              business_id=business_obj)
    else:
        obj.networth_py = networth
        obj.unsecured_py = unsecured
        obj.secured_py = secured
        obj.per_unsecured_upon_secured_py  = res
        obj.debt_upon_equity_py  = res1
        obj.save()

    data = {'res': res, 'res1': res1}
    return JsonResponse(data)

def financial_calculations_eighteen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    networth = request.GET.get('networth')
    print(networth)
    print(type(networth))
    unsecured = request.GET.get('unsecured')
    secured = request.GET.get('secured')
    res = round((float(unsecured) / (float(unsecured)+float(secured))), 2)
    print(res)
    res1 = round((float(unsecured) + float(secured)) / float(networth), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(networth_cy=networth, unsecured_cy=unsecured, secured_cy=secured, percentage_of_unsecuredloan_upon_totalloan_one_cy=res, debt_upon_equity_one_cy=res1,
                                              business_id=business_obj)
    else:
        obj.networth_cy = networth
        obj.unsecured_cy = unsecured
        obj.secured_cy = secured
        obj.per_unsecured_upon_secured_cy = res
        obj.debt_upon_equity_cy = res1
        obj.save()

    data = {'res': res, 'res1': res1}
    return JsonResponse(data)

def financial_calculations_nineteen(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    networth = request.GET.get('networth')
    print(networth)
    print(type(networth))
    unsecured = request.GET.get('unsecured')
    secured = request.GET.get('secured')
    res = round((float(unsecured) / (float(unsecured)+float(secured))), 2)
    print(res)
    res1 = round((float(unsecured) + float(secured)) / float(networth), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(networth_lqy=networth, unsecured_lqy=unsecured, secured_lqy=secured, percentage_of_unsecuredloan_upon_totalloan_one_lqy=res, debt_upon_equity_one_lqy=res1,
                                              business_id=business_obj)
    else:
        obj.networth_lqy = networth
        obj.unsecured_lqy = unsecured
        obj.secured_lqy = secured
        obj.per_unsecured_upon_secured_lqy = res
        obj.debt_upon_equity_lqy = res1
        obj.save()

    data = {'res': res, 'res1': res1}
    return JsonResponse(data)

def financial_calculations_twenty(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    networth = request.GET.get('networth')
    print(networth)
    print(type(networth))
    unsecured = request.GET.get('unsecured')
    secured = request.GET.get('secured')
    res = round((float(unsecured) / (float(unsecured)+float(secured))), 2)
    print(res)
    res1 = round((float(unsecured) + float(secured)) / float(networth), 2)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(networth_lqy=networth, unsecured_lqy=unsecured, secured_lqy=secured, percentage_of_unsecuredloan_upon_totalloan_one_lqy=res, debt_upon_equity_one_lqy=res1,
                                              business_id=business_obj)
    else:
        obj.networth_sqy = networth
        obj.unsecured_sqy = unsecured
        obj.secured_sqy = secured
        obj.per_unsecured_upon_secured_sqy = res
        obj.debt_upon_equity_sqy = res1
        obj.save()

    data = {'res': res, 'res1': res1}
    return JsonResponse(data)

def financial_calculations_twenty_one(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    recievable = request.GET.get('recievable')
    res = round((365/float(sales)) * float(recievable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_ly=sales, recievable_ly=recievable, debtors_upon_sales_ly=res,
                                              business_id=business_obj)
    else:
        obj.sales_ly = sales
        obj.recievable_ly = recievable
        obj.debtors_upon_sales_ly = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_two(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    recievable = request.GET.get('recievable')
    res = round((365 / float(sales)) * float(recievable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_py=sales, recievable_py=recievable, debtors_upon_sales_py=res,
                                              business_id=business_obj)
    else:
        obj.sales_ly = sales
        obj.recievable_py = recievable
        obj.debtors_upon_sales_py = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_three(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    recievable = request.GET.get('recievable')
    res = round((365 / float(sales)) * float(recievable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_cy=sales, recievable_cy=recievable, debtors_upon_sales_cy=res,
                                              business_id=business_obj)
    else:
        obj.sales_cy = sales
        obj.recievable_cy = recievable
        obj.debtors_upon_sales_cy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_four(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    recievable = request.GET.get('recievable')
    res = round((365 / float(sales)) * float(recievable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_lqy=sales, recievable_lqy=recievable, debtors_upon_sales_lqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_lqy = sales
        obj.recievable_lqy = recievable
        obj.debtors_upon_sales_lqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_five(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    recievable = request.GET.get('recievable')
    res = round((365 / float(sales)) * float(recievable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_sqy=sales, recievable_sqy=recievable, debtors_upon_sales_sqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_sqy = sales
        obj.recievable_sqy = recievable
        obj.debtors_upon_sales_sqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_six(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    payeable = request.GET.get('payeable')
    res = round((365 / float(sales)) * float(payeable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_ly=sales, payeable_ly=payeable, credit_upon_purchase_ly=res,
                                              business_id=business_obj)
    else:
        obj.sales_ly = sales
        obj.payeable_ly = payeable
        obj.credit_upon_purchase_ly = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_seven(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    payeable = request.GET.get('payeable')
    res = round((365 / float(sales)) * float(payeable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_py=sales, payeable_py=payeable, credit_upon_purchase_py=res,
                                              business_id=business_obj)
    else:
        obj.sales_py = sales
        obj.payeable_py = payeable
        obj.credit_upon_purchase_py = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_eight(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    payeable = request.GET.get('payeable')
    res = round((365 / float(sales)) * float(payeable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_cy=sales, payeable_cy=payeable, credit_upon_purchase_cy=res,
                                              business_id=business_obj)
    else:
        obj.sales_cy = sales
        obj.payeable_cy = payeable
        obj.credit_upon_purchase_cy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_twenty_nine(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    payeable = request.GET.get('payeable')
    res = round((365 / float(sales)) * float(payeable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_lqy=sales, payeable_lqy=payeable, credit_upon_purchase_lqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_lqy = sales
        obj.payeable_lqy = payeable
        obj.credit_upon_purchase_lqy = res
        obj.save()

    data = {'res': res}
    return JsonResponse(data)

def financial_calculations_thirty(request):
    business_id = request.session['business_id']
    print("In financial calculations", business_id)
    print("In financial calculations")
    sales = request.GET.get('sales')
    print(sales)
    print(type(sales))
    payeable = request.GET.get('payeable')
    res = round((365 / float(sales)) * float(payeable), 2)
    print(res)
    business_obj = Business.objects.get(business_id=business_id)
    print(business_obj)
    try:
        obj =Financial_calculations.objects.get(business_id=business_id)
    except Financial_calculations.DoesNotExist:
        Financial_calculations.objects.create(sales_sqy=sales, payeable_sqy=payeable, credit_upon_purchase_sqy=res,
                                              business_id=business_obj)
    else:
        obj.sales_sqy = sales
        obj.payeable_sqy = payeable
        obj.credit_upon_purchase_sqy = res
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

def investor_pending_form(request,pk):
    print("IN INVESTOR PENDING FORM",pk)
    context = {'pk':pk}
    return render(request, 'InvestorDashboards/investor_pending_form.html',context)

def investor_approved_form(request,pk):
    context = {'pk':pk}
    return render(request, 'InvestorDashboards/investor_approved_form.html', context)


def create_entity(request):
    if request.method == 'POST':
        form = EntityForm(request.POST, request.FILES)
        if form.is_valid():
            new_entity=form.save()
            image = new_entity.company_logo
            # new_entity.save()
            print(image, type(image))
            return redirect('investor')
    else:
        form = EntityForm()
    return render(request, 'Business/create-entity.html', {'form': form})
# return redirect('registered_businesses')

# def create_entity_2(request):
#     if request.method == 'POST':
#         form = EntityForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_entity=form.save()
#             image = new_entity.company_logo
#             new_entity.save()
#             print(image, type(image))
#             return redirect('create-entity-investor')
#     else:
#         form = EntityForm()
#     return render(request, 'Business/create-entity.html', {'form': form})
# return redirect('registered_businesses')


def create_entity_business(request):
    entities = Entity.objects.all()
    business = Business.objects.all()
    form = EntityBusinessForm()

    if request.method == 'POST':
        form = EntityBusinessForm(request.POST)
        if form.is_valid():
            entity_id = request.POST['entity']
            business_id = request.POST['business']
            entity_obj = Entity.objects.get(entity_id=entity_id)
            business_obj = Business.objects.get(business_id=business_id)
            applicable_roi = form.cleaned_data['applicable_roi']
            benchmark_roi = form.cleaned_data['benchmark_roi']
            special_roi = form.cleaned_data['special_roi']
            sector_base_rate = form.cleaned_data['sector_base_rate']
            sector_risk_premium = form.cleaned_data['sector_risk_premium']
            business_risk_premium = form.cleaned_data['business_risk_premium']
            entity_risk_premium = form.cleaned_data['entity_risk_premium']
            applicable_discount_rate = form.cleaned_data['applicable_discount_rate']
            applicable_platform_fee = form.cleaned_data['applicable_platform_fee']
            sub_limit = form.cleaned_data['sub_limit']
            available_sub_limit = form.cleaned_data['available_sub_limit']
            approved_credit_period = form.cleaned_data['approved_credit_period']
            margin_days = form.cleaned_data['margin_days']
            try:
                mapping_object = EntityBusinessROIMapping(entity_id = entity_id, business_id = business_id)
                values = {'entity_id' : entity_id, 'business_id' : business_id, 'entity_obj' : entity_obj, 'business_obj' : business_obj, 'applicable_roi' : applicable_roi, 'benchmark_roi' : benchmark_roi, 'special_roi' : special_roi, 'sector_base_rate' : sector_base_rate, 'sector_risk_premium' : sector_risk_premium, 'business_risk_premium' : business_risk_premium, 'entity_risk_premium' : entity_risk_premium, 'applicable_discount_rate' : applicable_discount_rate, 'applicable_platform_fee' : applicable_platform_fee, 'sub_limit' : sub_limit, 'available_sub_limit' : available_sub_limit, 'approved_credit_period' : approved_credit_period, 'margin_days' : margin_days}
                for k,v in values.items():
                    setattr(mapping_object, k ,v)
                mapping_object.save()
            except:
                EntityBusinessROIMapping.objects.create(entity_id = entity_obj, business_id = business_obj, applicable_roi = applicable_roi, benchmark_roi = benchmark_roi, special_roi = special_roi, sector_base_rate = sector_base_rate, sector_risk_premium = sector_risk_premium, business_risk_premium = business_risk_premium, entity_risk_premium = entity_risk_premium, applicable_discount_rate = applicable_discount_rate, applicable_platform_fee = applicable_platform_fee, sub_limit = sub_limit, available_sub_limit = available_sub_limit, approved_credit_period = approved_credit_period, margin_days = margin_days)
            business_obj.status = "APPROVED"
            business_obj.save()
            return redirect('registered_businesses')

        return redirect('create-entity-business')
    return render(request, 'Business/create-entity-business.html', {'form': form, 'entities' : entities, 'business':business})


def create_entity_investor(request):
    entities = Entity.objects.all()
    investors = Investor.objects.all()
    form = EntityInvestorForm()
    if request.method == 'POST':
        form = EntityInvestorForm(request.POST)
        if form.is_valid():
            # 'entity_id' :entity_id, 'investor_id' :investor_id, 'entity_obj' :entity_obj, 'investor_obj' :investor_obj, 'applicable_platform_fee' :applicable_platform_fee, 'applicable_ror' :applicable_ror, 
            entity_id = request.POST['entity']
            investor_id = request.POST['investor']
            entity_obj = Entity.objects.get(entity_id=entity_id)
            investor_obj = Investor.objects.get(investor_id=investor_id)
            applicable_platform_fee = form.cleaned_data['applicable_platform_fee']
            applicable_ror = form.cleaned_data['applicable_ror']
            EntityInvestorRORMapping.objects.create(investor_id=investor_obj, entity_id=entity_obj,applicable_platform_fee=applicable_platform_fee, applicable_ror=applicable_ror)
            investor_obj.status = "APPROVED"
            investor_obj.save()
            return redirect('approved_investor')
    return render(request, 'Business/create-entity-investor.html', {'form': form, 'entities' : entities, 'investors':investors})
