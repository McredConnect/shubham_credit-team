from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib import messages

# Create your views here.
from Investors.models import Business
from tests.models import *
from InvestorDashboards.models import *


def bank_detail(request):
    return render(request, 'InvestorDashboards/bankdetail.html')


def business_detail(request):
    return render(request, 'InvestorDashboards/businessdetail.html')


def business(request):
    return render(request, 'InvestorDashboards/business.html')


def business_info(request):
    return render(request, 'InvestorDashboards/businessinfo.html')


def bank_statement_two(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('bank_state1', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    bank_statement = BankstatementDetails_new.objects.filter(business_id=business_id)
    bank_statement_details = BankstatementDetails_new.objects.filter(business_id=business_id) & BankstatementDetails_new.objects.filter(Type="detail")

    if request.method == "POST":
        bank_name = request.POST['bankname']
        acc_num = request.POST['acc_num']
        acc_type = request.POST['acc_type']
        # business_obj = Business.objects.get(business_id=business_id)
        obj = BankstatementDetails_new.objects.create(business_id=business_obj, bank_name=bank_name, AC_No=acc_num, AC_Type=acc_type)

        if obj:
            return redirect('bank_statement_two')

    return render(request, 'business_dashboard/bankstatement.html', {'bankstatement': bank_statement, 'bank_statement_details':bank_statement_details})

def bank_statement_details(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('bank_state', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    if request.method == "POST":
        sel_ac = request.POST['bankacno']
        from_date = request.POST['fromDate']
        to_date = request.POST['to_date']
        bank_state = request.FILES.get('statement')
        type = request.POST['statement']

        obj = BankstatementDetails_new.objects.filter(AC_No=sel_ac)
        print(obj)
        for i in obj:
            i.from_date = from_date
            i.To_date = to_date
            i.input_file = bank_state
            i.Type = type
            i.save()
        # business_obj = Business.objects.get(business_id=business_id)
        # obj = BankstatementDetails_new.objects.create(business_id=business_obj, AC_No=sel_ac, from_date=from_date, To_date=to_date, input_file=bank_state, Type=type)
        return redirect('bank_statement_two')
    # return render(request, 'InvestorDashboards/bankstatement.html')
def index(request):
    return render(request,'InvestorDashboards/index_new.html')

def company_details(request):
    print('in companydetails')
    business_id = Business.objects.get(user_id=request.user).business_id
    print('comde',business_id)
    business_obj = Business.objects.get(business_id=business_id)
    print('business_obj_com',business_obj)
    cususer_obj = CustomUser.objects.get(username=str(request.user))

    # print(BusinessProfile_obj)
    business_obj.status = 'New'
    business_obj.save()
    turnover = business_obj.turnover
    company_name = cususer_obj.organisation
    entity = business_obj.type_of_business
    cin_llp = business_obj.CIN_LLP_no
    sector = business_obj.sector
    city = business_obj.city
    state = business_obj.state
    try:
        address = business_obj.business_address
        address1 = address[address.index("['") + len("['"): address.index("', '")]
        address2 = address[address.index(", '") + len(", '"): address.index("', '", address.index(", '") + len(", '"))]
        pincode = address[address.index(", '", address.index(address2) + len(address2)) + len(", '"): address.index("']", )]
    except:
        address=" "
        address1=" "
        address2=" "
        pincode=" "


    try:
        moa_object = BusinessDetails_test_new.objects.get(file_name="MOA/AOA", business_id=business_obj)
        moa_aoa = moa_object.input_file
    except:
        moa_aoa = None
    try:
        coi_object = BusinessDetails_test_new.objects.get(business_id=business_obj, file_name="COI/LLP Certificate")
        coi = coi_object.input_file
    except:
        coi=None
    try:
        address_object = BusinessDetails_test_new.objects.get(business_id=business_obj, file_name="COMPANY ADDRESS PROOF")
        add_proof = address_object.input_file
    except:
        add_proof = None


    try:
        BusinessProfile_obj = BusinessProfile.objects.get(business_id=business_id)
        about = BusinessProfile_obj.brief
        file = BusinessProfile_obj.input_file
    except:
        about= " "
        file = None
    print(file)
    print(about)
    # file = BusinessProfile_obj.input_file
    if request.method == 'POST':
        company_name = request.POST['company']
        turnover = request.POST['turnover']
        entity = request.POST['entity']
        cin_llp = request.POST['cin_llp']
        sector = request.POST['sector']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        moa_aoa = request.FILES.get('moa_aoa')
        coi = request.FILES.get('coi')
        add_proof = request.FILES.get('add_proof')
        aboutc = request.POST['about']
        about_file = request.FILES.get('about_file')
        cususer_obj.organisation = company_name
        cususer_obj.save()
        business_obj.turnover = turnover
        business_obj.type_of_business = entity
        business_obj.CIN_LLP_no = cin_llp
        business_obj.sector = sector = sector
        business_obj.business_address = [address1, address2, pincode]
        business_obj.city = city
        business_obj.state = state
        business_obj.save()
        # BusinessDetails_test_obj = BusinessDetails_test.objects.filter(business_id=business_id)
        # BusinessProfile_obj = BusinessProfile.objects.get(business_id=business_id)
        try:
            moa_object = BusinessDetails_test_new.objects.get(file_name="MOA/AOA", business_id=business_obj)
        except:
            moa_object = BusinessDetails_test_new.objects.create(business_id=business_obj, file_name="MOA/AOA")
        try:
            coi_object = BusinessDetails_test_new.objects.get(business_id=business_obj, file_name="COI/LLP Certificate")
        except:
            coi_object = BusinessDetails_test_new.objects.create(business_id=business_obj, file_name="COI/LLP Certificate")
        try:
            address_object = BusinessDetails_test_new.objects.get(business_id=business_obj,file_name="COMPANY ADDRESS PROOF")
        except:
            address_object = BusinessDetails_test_new.objects.create(business_id=business_obj, file_name="COMPANY ADDRESS PROOF")

        moa_object.input_file = moa_aoa
        coi_object.input_file = coi
        address_object.input_file = add_proof
        moa_object.username = business_obj.business_name
        coi_object.username = business_obj.business_name
        address_object.username = business_obj.business_name
        moa_object.save()
        coi_object.save()
        address_object.save()

        # if len(BusinessDetails_test_obj) == 0:
        #     # create
        #     BusinessDetails_test.objects.create(business_id=business_obj, file_name="MOA/AOA", input_file=moa_aoa)
        #     BusinessDetails_test.objects.create(business_id=business_obj, file_name="COI/LLP Certificate",
        #                                         input_file=coi)
        #     BusinessDetails_test.objects.create(business_id=business_obj, file_name="COMPANY ADDRESS PROOF",
        #                                         input_file=add_proof)
        #     pass
        # else:
        #     object1 = BusinessDetails_test_obj.first()
        #     object1.file_name ="MOA/AOA"
        #     object1.input_file = moa_aoa
        #     object1.save()
        #     # update
        #     pass
        try:
            about_object = BusinessProfile.objects.get(business_id=business_obj)
        except:
            about_object = BusinessProfile.objects.create(business_id=business_obj)

        about_object.brief=aboutc
        about_object.input_file=about_file
        about_object.save()

        # if len(BusinessProfile_obj) == 0:
        #     BusinessProfile.objects.create(business_id=business_obj, brief=aboutc, input_file=about_file)
        # else:
        #     obj1 = BusinessProfile_obj.first()
        #     obj1.brief = aboutc
        #     obj1.input_file = about_file
        #     obj1.save()    'address1':address1, 'address2':address2, 'pincode':pincode,
        return redirect('company_details_two')

    context = {'company_name':company_name, 'entity': entity,'turnover':turnover,'cin_llp':cin_llp,
                   'sector':sector, 'city':city, 'state': state,'about':about, 'file':file,
                'moa_aoa':moa_aoa, 'coi':coi, 'add_proof':add_proof,'address1':address1, 'address2':address2, 'pincode':pincode}
    return render(request, 'business_dashboard/companydetails.html',context)



def gst_details(request):
    print("in gst_details")
    # business_id = request.session['business_id']
    business_id = Business.objects.get(user_id=request.user).business_id
    print('gst', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    pan = business_obj.business_pan_card
    print('gstob',business_obj)
    # business_id = request.session['business_id']

    gst_details = GSTDetails_test_new.objects.filter(business_id=business_id) & GSTDetails_test_new.objects.filter(gst_type='certificate')
    gst_details_gstr_one = GSTDetails_test_new.objects.filter(business_id=business_id) & GSTDetails_test_new.objects.filter(gst_type='GSTR_1')
    gst_details_gstr_two_a = GSTDetails_test_new.objects.filter(business_id=business_id) & GSTDetails_test_new.objects.filter(gst_type='GSTR_2A')
    gst_details_gstr_three_b = GSTDetails_test_new.objects.filter(business_id=business_id) & GSTDetails_test_new.objects.filter(gst_type='GSTR_3B')

    context = {'gstdetails': gst_details, 'gst_details_gstr_one': gst_details_gstr_one, 'gst_details_gstr_two_a': gst_details_gstr_two_a, 'gst_details_gstr_three_b':gst_details_gstr_three_b, 'pan':pan}
    if request.method == "POST":
        gst_num = request.POST['gst_no']
        gst_cert = request.FILES.get('gst_certificate')
        state = request.POST['state']
        type = request.POST['type']
        # business_obj = Business.objects.get(business_id=business_id)
        obj = GSTDetails_test_new.objects.create(business_id=business_obj, gst_No=gst_num, state=state, input_file=gst_cert, gst_type=type)
        if obj:
            return redirect('gst_details')
        return redirect('bank_statement')
    return render(request, 'business_dashboard/gstdetails.html', context)


def gstdetails_one(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('gst', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    print('gstob', business_obj)
    if request.method == 'POST':
        gstno = request.POST['gst_num']
        from_date = request.POST['fromdate']
        to_date = request.POST['todate']
        file = request.FILES.get('document')
        type = request.POST['type']
        # business_obj = Business.objects.get(business_id=business_id)
        obj = GSTDetails_test_new.objects.create(business_id=business_obj, gst_No=gstno, fromdate=from_date, Todate=to_date, input_file=file, gst_type=type)
        return redirect('gst_details')

def gstdetails_two_A(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('gst', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    print('gstob', business_obj)
    if request.method == 'POST':
        gstno = request.POST['gst_num']
        from_date = request.POST['fromdate1']
        to_date = request.POST['todate1']
        file = request.FILES.get('document1')
        type = request.POST['type']
        # business_obj = Business.objects.get(business_id=business_id)
        obj = GSTDetails_test_new.objects.create(business_id=business_obj, gst_No=gstno, fromdate=from_date, Todate=to_date, input_file=file, gst_type=type)
        return redirect('gst_details')

def gstdetails_three_b(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('gst', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    print('gstob', business_obj)
    if request.method == 'POST':
        gstno = request.POST['gst_num']
        from_date = request.POST['fromdate2']
        to_date = request.POST['todate2']
        file = request.FILES.get('document2')
        type = request.POST['type']
        # business_obj = Business.objects.get(business_id=business_id)
        obj = GSTDetails_test_new.objects.create(business_id=business_obj, gst_No=gstno, fromdate=from_date, Todate=to_date, input_file=file, gst_type=type)
        return redirect('gst_details')



def pan_details(request):
    print("In pan details")
    business_id = Business.objects.get(user_id=request.user).business_id
    print('pan', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    context = {}
    pan_num = business_obj.business_pan_card
    try:
        aadhaar_num = business_obj.business_udyog_adhaar
    except:
        aadhaar_num = " "
    try:
        pan_obj = BusinessDetails_test_new.objects.get(file_name="PAN CARD", business_id=business_obj)
        pan_card = pan_obj.input_file

    except:
        pan_card = None
    try:
        aadhaar_object = BusinessDetails_test_new.objects.get(business_id=business_obj, file_name="AADHAAR CARD")
        aadhaar_card = aadhaar_object.input_file
    except:
        aadhaar_card=None
    if request.method == 'POST':
        pan_num = request.POST['pan_num']
        pan_card = request.FILES.get('pan_card')
        aadhaar_num = request.POST['aadhaar_num']
        aadhaar_card = request.FILES.get('aadhaar_card')
        business_obj.business_pan_card = pan_num
        business_obj.business_udyog_adhaar = aadhaar_num
        business_obj.save()
        # obj = Business.objects.create(business_pan_card=pan_num, business_udyog_adhaar=aadhaar_num)
        # print(obj)
        # business_id = obj.business_id
        # print(business_id)
        # business_obj = Business.objects.get(business_id=business_id)
        # print(business_obj)
        try:
            pan_object = BusinessDetails_test_new.objects.get(file_name="PAN CARD", business_id=business_obj, )
        except:
            pan_object = BusinessDetails_test_new.objects.create(business_id=business_obj, file_name="PAN CARD",)
        try:
            aadhaar_object = BusinessDetails_test_new.objects.get(business_id=business_obj, file_name="AADHAAR CARD")
        except:
            aadhaar_object = BusinessDetails_test_new.objects.create(business_id=business_obj, file_name="AADHAAR CARD")
        pan_object.input_file = pan_card
        pan_object.username=business_obj.business_name
        print(pan_object.input_file)
        aadhaar_object.input_file = aadhaar_card
        aadhaar_object.username=business_obj.business_name
        pan_object.save()
        aadhaar_object.save()
        return redirect('pan_details')
    context = {'pan_num':pan_num, 'aadhaar_num':aadhaar_num,'pan_card':pan_card,'aadhaar_card':aadhaar_card}
    return render(request, 'business_dashboard/pandetails.html', context)



def financials(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('financials', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    financials = Financialdetail_test.objects.filter(business_id=business_id)
    if request.method == 'POST':
        from_Date = request.POST['fromdate']
        to_Date = request.POST['todate']
        status = request.POST['status']
        file = request.FILES.get('uploaded_file')
        # business_obj = Business.objects.get(business_id=business_id)
        obj = Financialdetail_test.objects.create(business_id=business_obj, from_date=from_Date, To_date=to_Date, input_file=file, status=status)
        if obj:
            return redirect('financials')

    return render(request, 'business_dashboard/financials.html', {'financials': financials})

def customers(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('customer', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    customer_details = Customerdetails.objects.filter(business_id=business_id)
    customer_obj = Customerdetails.objects.filter(business_id=business_id).first()
    try:
        average_monthly_sale = customer_obj.average_monthly_sale
        total_annual_sale = customer_obj.total_annual_sale
    except:
        average_monthly_sale=0
        total_annual_sale=0
    if request.method == 'POST':
        name = request.POST['name_of_customer']
        yearly_sales = request.POST['yearly_sales']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        file = request.FILES.get('inp_file')
        # total_annual_sales = request.POST['total_annual_sales']
        # avg_monthly_sales = request.POST['avg_monthly_sales']
        # business_obj = Business.objects.get(business_id=business_id)  , 'average_monthly_sale':average_monthly_sale, 'total_annual_sale':total_annual_sale}
        obj = Customerdetails.objects.create(business_id=business_obj, name=name, per_tweleve_month_sale=yearly_sales, fromdate=from_date, todate=to_date, input_file=file)
        if obj:
            return redirect('customers')
    return render(request, 'business_dashboard/customers.html', {'customer_details': customer_details, 'average_monthly_sale':average_monthly_sale, 'total_annual_sale':total_annual_sale})

def customers2(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('customer2', business_id)

    context = {}
    if request.method == 'POST':
        total_annual_sales = request.POST['total_annual_sales']
        print(total_annual_sales)
        avg_monthly_sales = request.POST['avg_monthly_sales']
        print(avg_monthly_sales)
        business_obj = Customerdetails.objects.filter(business_id=business_id).first()
        try:
            business_obj.average_monthly_sale = avg_monthly_sales
            business_obj.total_annual_sale = total_annual_sales
            business_obj.save()
        except:
            business_obj.average_monthly_sale =0
            business_obj.total_annual_sale=0
            business_obj.total_annual_sale=0
            business_obj.save()
    return redirect('customers')



def suppliers(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('supplier', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    supplier_details = Suppliersdetails_new.objects.filter(business_id=business_id)
    supplier_obj = Suppliersdetails_new.objects.filter(business_id=business_id).first()
    try:
        avg_monthly_purchase = supplier_obj.avg_monthly_purchase
        Total_annual_purchase = supplier_obj.Total_annual_purchase
    except:
        avg_monthly_purchase=0
        Total_annual_purchase=0
    if request.method == 'POST':
        name = request.POST['name_of_supplier']
        yearly_purchase = request.POST['yearly_purchase']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        file = request.FILES.get('inp_file')

        # business_obj = Business.objects.get(business_id=business_id)
        obj = Suppliersdetails_new.objects.create(business_id=business_obj, name=name, last_tweleve_month_sale=yearly_purchase,
                                             fromdate=from_date, todate=to_date, input_file=file)
        if obj:
            return redirect('suppliers')
    return render(request, 'business_dashboard/suppliers.html', {'supplier_details': supplier_details,'Total_annual_purchase':Total_annual_purchase, 'avg_monthly_purchase':avg_monthly_purchase})
#
def suppliers2(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('supplier2', business_id)
    # business_obj = Business.objects.get(business_id=business_id)
    if request.method == 'POST':
        total_annual_purchase = request.POST['total_annual_purchase']
        print(total_annual_purchase)
        avg_monthly_purchase = request.POST['avg_monthly_purchase']
        print(avg_monthly_purchase)
        try:
            business_obj = Suppliersdetails_new.objects.get(business_id=business_id)
            business_obj.avg_monthly_purchase = avg_monthly_purchase
            business_obj.Total_annual_purchase = total_annual_purchase
            business_obj.save()
        except:
            business_obj = None
            business_obj.avg_monthly_purchase=0
            business_obj.Total_annual_purchase=0
            business_obj.save()
        return redirect('suppliers')

def registration(request):
    return render(request, 'business_dashboard/registration.html')


def home(request):
    print("before company detail", request.session['business_id'])
    return redirect('company_details')

def as_26(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('as_26', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    as_26_details = As26detail.objects.filter(business_id=business_id)
    if request.method == 'POST':
        report_name = request.POST['report_name']
        fromdate = request.POST['from_date']
        todate = request.POST['to_date']
        file = request.FILES.get('file')
        # business_obj = Business.objects.get(business_id=business_id)
        obj = As26detail.objects.create(business_id=business_obj, name_of_document=report_name, fromdate=fromdate, todate=todate, input_file=file)
        if obj:
            return redirect('as_26')

        return redirect('creditrating')

    return render(request, 'business_dashboard/as_26.html', {'as_26':as_26_details})

def creditrating(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('credit', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    creditrating = CreditRating_test.objects.filter(business_id=business_id)
    if request.method == 'POST':
        rating_agency = request.POST['agency']
        rating_date = request.POST['date']
        rating = request.POST['rating']
        file = request.FILES.get('upload_file')
        # business_obj = Business.objects.get(business_id=business_id)
        obj = CreditRating_test.objects.create(business_id=business_obj, ratingagency=rating_agency, date_of_rating=rating_date, rating=rating, input_file=file)
        if obj:
            return redirect('creditrating')
    return render(request, 'business_dashboard/creditratings.html', {'credit_rating' : creditrating})

def shareholding_two(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('shareholding', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    shareholdings = Shareholding.objects.filter(business_id=business_id)
    if request.method == 'POST':
        name = request.POST['sname']
        percentage = request.POST['percentage']
        file = request.FILES.get('uploaded_file')
        # print(file)
        # business_obj = Business.objects.get(business_id=business_id)
        obj = Shareholding.objects.create(business_id=business_obj, nameofshareholder=name, percentage_of_shareholding=percentage, input_file=file)
        if obj:
            return redirect('shareholding_two')
        # return redirect('directors')
    return render(request, 'business_dashboard/shareholding.html',{'shareholding':shareholdings})

# def shareholding1(request):
#     business_id = request.session['business_id']
#     print(business_id)
#     # shareholdings1 = Shareholding.objects.filter(business_id=business_id)
#     if request.method == 'POST':
#         file = request.FILES.get('uploaded_file')
#         print(file)
#         business_obj = Shareholding.objects.get(business_id=business_id)
#         business_obj.input_file = file
#         business_obj.save()
#         return redirect('shareholding')
#     return render(request, 'InvestorDashboards/shareholding.html',{'shareholding1':shareholdings1})


def directors(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('directors', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    directors = Director_list.objects.filter(business_id=business_id)
    status = None
    if request.method == 'POST':
        name = request.POST['name_of_director']
        address = request.POST['address']
        din_number = request.POST['din_number']
        pan_number = request.POST['pan_number']
        pan_file = request.FILES.get('pan_card')
        aadhaar_number = request.POST['aadhaar_num']
        aadhaar_file = request.FILES.get('aadhaar_card')
        # business_obj = Business.objects.get(business_id=business_id)
        obj = Director_list.objects.create(business_id=business_obj, name_of_the_director=name, address=address, DIN_number=din_number,Pan_number=pan_number, input_file=pan_file, Aadhar_number=aadhaar_number, Aadhar_file=aadhaar_file)

    return render(request, 'business_dashboard/directors.html', {'directors': directors})

def debt(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('debt', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    debt = DebtProfile_new.objects.filter(business_id=business_id)
    if request.method == 'POST':
        name_of_lender = request.POST['lender_name']
        type_of_loan = request.POST['type']
        loan_amt = request.POST['loan_amt']
        outstanding_amount = request.POST['outstanding_amt']
        interest_rate = request.POST['interest_rate']
        file = request.FILES.get('file')

        # business_obj = Business.objects.get(business_id=business_id)
        obj = DebtProfile_new.objects.create(business_id=business_obj, name_of_lender=name_of_lender, type_of_loan=type_of_loan, outstanding_amount=outstanding_amount, amount_of_loan=loan_amt, rate_of_interest=interest_rate, input_file=file)
        if obj:
            return redirect('debt')
    return render(request, 'business_dashboard/debt.html', {'debt': debt})

def auth_userdetails(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('userdetails', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    user_details = AuthorisedPerson_details_new.objects.filter(business_id=business_id)
    if request.method == 'POST':
        name = request.POST['name_of_person']
        designation = request.POST['designation']
        email = request.POST['email']
        phone = request.POST['phone']
        mobile = request.POST['mobile']
        location = request.POST['location']
        pan = request.FILES.get('pancard')
        aadhaar = request.FILES.get('aadhaar')
        if len(mobile) != 10:
            messages.error(request, 'username or password not correct')
        # business_obj = Business.objects.get(business_id=business_id)
        obj = AuthorisedPerson_details_new.objects.create(business_id=business_obj, name=name, designation=designation, email=email, phone=phone, mobile=mobile, location=location, pan=pan, aadhaar=aadhaar)
    return render(request, 'business_dashboard/userdetails.html', {'user_details':user_details})

def bank_acc_details(request):
    business_id = Business.objects.get(user_id=request.user).business_id
    print('ban_acc', business_id)
    business_obj = Business.objects.get(business_id=business_id)
    business = Business.objects.filter(business_id=business_id)
    if request.method == 'POST':
        bank_name = request.POST['bank_name']
        ac_no = request.POST['ac_no']
        ifsc_code = request.POST['ifsc_code']
        check = request.FILES.get('check')
        # business_obj = Business.objects.get(business_id=business_id)
        print(business_obj)
        business_obj.business_bank_name = bank_name
        business_obj.business_bank_account_no = ac_no
        business_obj.business_bank_account_IFSC_code = ifsc_code
        business_obj.business_bank_account_cancelled_cheque = check
        business_obj.save()
    return render(request, 'business_dashboard/bank_acc_details.html', {'business': business})


def test1(request):
    business = Business.objects.all()
    return render(request, 'business_dashboard/test1.html', {'business': business})


def test2(request, pk):
    # obj = get_object_or_404(BusinessDetails_test, pk)
    obj = BusinessDetails_test.objects.get(business_id=pk)
    print(obj)
    return render(request, 'business_dashboard/test2.html', {'obj': obj})


def user_logout(request):
    logout(request)
    return redirect('mcred_login')



