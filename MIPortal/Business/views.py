from django.shortcuts import render, redirect, get_object_or_404
from Investors.models import *
from django.contrib import messages
from datetime import timedelta, date
from Investors.views import format_amount
from MIPortal.settings import MEDIA_ROOT, MEDIA_URL
from .forms import *

# Create your views here.

def bank_account(request):
    user = CustomUser.objects.get(username=request.user)
    business_obj = Business.objects.get(user_id_id=user)
    user_name = user.first_name + ' ' + user.last_name
    company_name = user.organisation
    balance = round(business_obj.escrow_balance, 2)
    account_no = business_obj.business_bank_account_no
    bank_name = business_obj.business_bank_name
    ifsc_code = business_obj.business_bank_account_IFSC_code
    return render(request, 'Business/bank-account.html', {'user_name':user_name, 'company_name':company_name, 'balance':balance, 'account_no':account_no,'bank_name':bank_name, 'ifsc_code':ifsc_code})


def bank_account_withdraw(request):
    return render(request, 'Business/bankaccount-withdraw.html')


def create_entity(request):
    if request.method == 'POST':
        form = EntityForm(request.POST, request.FILES)
        if form.is_valid():
            new_entity=form.save()
            image = new_entity.company_logo
            print(image, type(image))
    else:
        form = EntityForm()
    return render(request, 'Business/create-entity.html', {'form': form})


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
            return redirect('create-entity-investor')
    return render(request, 'Business/create-entity-investor.html', {'form': form, 'entities' : entities, 'investors':investors})


def dashboard(request, **kwargs):
    user = CustomUser.objects.filter(username=request.user).first()
    business_obj = Business.objects.filter(user_id_id=user).first()
    credit_limit = float(business_obj.facility_approved_amount)
    available_limit = float(business_obj.available_facility_limit)
    used_limit = credit_limit - available_limit
    invoice_objs = Invoice.objects.filter(business_id_id = business_obj.business_id)
    # for i in invoice_objs:
    new_invoices = Invoice.objects.filter(business_id_id = business_obj.business_id).filter(final_approval_status_verification='pending')
    live_invoices = Invoice.objects.filter(business_id_id = business_obj.business_id).filter(final_approval_status_verification='approved')
    financed_invoices = Invoice.objects.filter(business_id_id = business_obj.business_id).filter(invoice_subscription_status__gt=0)
    repaid_invoices = Invoice.objects.filter(business_id_id = business_obj.business_id).filter(status='repaid')
    total_funds_raised = 0.0
    for i in financed_invoices:
        total_funds_raised += i.invoice_total_investment
    total_repaid_amount = 0.0
    for i in repaid_invoices:
        total_repaid_amount += i.invoice_amount
    total_funds_raised = round(total_funds_raised, 2)
    total_repaid_amount = round(total_repaid_amount, 2)
    return render(request,'Business/dashboard.html', {'credit_limit': credit_limit, 'available_limit': available_limit, 'used_limit': used_limit, 'invoice_objs': invoice_objs,'new_invoices' : len(new_invoices), 'live_invoices' : len(live_invoices), 'financed_invoices' : len(financed_invoices), 'repaid_invoices' : len(repaid_invoices),'total_funds_raised' : format_amount(total_funds_raised), 'total_repaid_amount' : format_amount(total_repaid_amount), 'credit_limit_amount': format_amount(credit_limit), 'available_limit_amount': format_amount(available_limit), 'used_limit_amount': format_amount(used_limit)})


def edit_business(request):
    business = Business.objects.all()
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business_id = request.POST['business']
            new_business = form.save()
    return render(request, 'Business/edit-business.html', {'form':form, 'business':business})


def help_and_support(request):
    data = QuestionAnswer.objects.filter(user_type='business')
    return render(request,'Business/help-and-support.html', {'data':data})


def invoice(request):
    user = CustomUser.objects.get(username=request.user)
    business_obj = Business.objects.get(user_id_id=user)
    business_id = business_obj.business_id
    invoice_objs = Invoice.objects.filter(business_id_id = business_id)
    data = list()
    for i in invoice_objs:
        temp_list = list()
        invoice_id = i.invoice_id
        entity_name = i.entity_name
        upload_date = i.invoice_upload_date
        amount = i.invoice_amount
        amount_financed = i.invoice_total_investment
        entity_id = Entity.objects.get(entity_name=entity_name).entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id)
        platform_fee = roi_obj.applicable_platform_fee
        roi = roi_obj.applicable_roi
        tenure = (i.invoice_date + timedelta(days=roi_obj.approved_credit_period) - date.today()).days
        temp_list.extend((upload_date, entity_name, amount, amount_financed, platform_fee, roi, invoice_id, tenure))
        data.append(temp_list)
    return render(request,'Business/invoice.html', {'data':data})


def invoice_upload(request):
    print(request)
    print(request.user)
    if request.method == "POST":
        invoice_flag = True
        user = CustomUser.objects.filter(username=request.user).first()
        business_obj = Business.objects.filter(user_id_id=user).first()
        total_limit = business_obj.available_facility_limit
        print('USER:\t',request.user)
        total_invoice_amt = request.POST['totalamount']
        invoice_count = request.POST['totalcount']
        business_name = business_obj.business_name
        business_id = business_obj.business_id
        today = datetime.today().strftime("%Y-%m-%d")
        print('business_id',business_id)
        batch_values = list(Invoice.objects.values_list('batch_no',flat=True).distinct())
        if len(batch_values)> 0:
            batch_no = int(max(batch_values)) + 1
        else:
            batch_no = 1
        print('business_name',business_name)
        final_approval_status_verification = 'pending'

        for i in range(int(invoice_count)):
            entity = request.POST['entity' + str(i+1)]
            entity_id = Entity.objects.filter(entity_name = entity).first()
            roi_obj =EntityBusinessROIMapping.objects.get(business_id = business_obj.business_id, entity_id=entity_id)
            entity_limit = roi_obj.available_sub_limit
            invoice_amount = float(request.POST['amount' + str(i+1)])
            if entity_limit < invoice_amount or total_limit < invoice_amount:
                invoice_flag = False
                continue
            invoice_date = request.POST['date' + str(i+1)]
            invoice_date = date(*[int(item) for item in invoice_date.split('-')])
            invoice_pdf = request.FILES['pdf' + str(i+1)]
            applicable_discount_rate = roi_obj.applicable_discount_rate
            discounted_val = (applicable_discount_rate / 100) * invoice_amount
            print('discounted_val',discounted_val)
            applicable_roi = roi_obj.applicable_roi
            credit_period = roi_obj.approved_credit_period
            invoice_due_date = invoice_date + timedelta(days = credit_period)
            invoice_fundable_amount = round(invoice_amount - discounted_val, 2)
            Invoice.objects.create(invoice_amount = invoice_amount, entity_name = entity, invoice_pdf = invoice_pdf, invoice_upload_date = today, invoice_date = invoice_date, batch_invoice_amount = total_invoice_amt, batch_number_of_invoices =  invoice_count, batch_no = batch_no, business_name = business_name, applicable_ROI = applicable_roi, invoice_fundable_amount = invoice_fundable_amount, applicable_discount_rate = applicable_discount_rate, business_id = business_obj, invoice_due_date = invoice_due_date, applicable_gst_rate=18, final_approval_status_verification = final_approval_status_verification)
            business_obj.available_facility_limit -= invoice_amount
            roi_obj.available_sub_limit -= invoice_amount
            business_obj.save()
            roi_obj.save()
        if invoice_flag:
            message = 'Invoice Uploaded Successfully'
            messages.success(request, message)
        else:
            message = 'Some Invoices were Rejected due to Invoice Limit'
            messages.warning(request, message)
        return redirect('dashboard')
    else:
        user = CustomUser.objects.filter(username=request.user).first()
        business_obj = Business.objects.filter(user_id_id=user).first()
        entities = list()
        # add field
        balance = business_obj.available_facility_limit
        if balance is None:
            balance = 0.0
        roi_objs = EntityBusinessROIMapping.objects.filter(business_id = business_obj.business_id)
        # ans = list(roi_objs.values_list('entity_id', flat = True).distinct())
        data = list()
        for i in roi_objs:
            temp_list = list()
            entity = Entity.objects.get(entity_id = i.entity_id_id)
            entities.append(entity.entity_name)
            temp_list.append(entity.entity_name)
            temp_list.append(i.available_sub_limit)
            data.append(temp_list)
        return render(request, 'Business/invoice-upload.html',{'entities' : entities, 'balance':balance,'data': data, } )


def refer_and_earn(request):
    return render(request,'Business/refer-and-earn.html')


def transactions(request):
    user = CustomUser.objects.get(username=request.user)
    business_obj = Business.objects.get(user_id_id=user)
    business_id = business_obj.business_id
    invoice_objs = Invoice.objects.filter(business_id_id = business_obj.business_id)
    data = list()
    for i in invoice_objs:
        temp_list = list()
        entity_name = i.entity_name
        entity_id = Entity.objects.get(entity_name=entity_name).entity_id
        invoice_id = i.invoice_id
        transaction_objs = Transaction.objects.filter(invoice_id_id = invoice_id)
        net_amount = 0.0
        for j in transaction_objs:
            net_amount += j.settlement_amount_with_business
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id)
        upload_date = i.invoice_upload_date
        entity_name = i.entity_name
        amount = i.invoice_amount
        discount = i.applicable_discount_rate
        finance_amount = i.invoice_fundable_amount
        fee = roi_obj.applicable_platform_fee
        net_amount = round(net_amount, 2)
        tenure = (i.invoice_date + timedelta(days=roi_obj.approved_credit_period) - date.today()).days
        roi = roi_obj.applicable_roi
        temp_list.extend((invoice_id, upload_date, entity_name, amount, discount, finance_amount, fee, net_amount, tenure, roi))
        data.append(temp_list)
    return render(request,'Business/transactions.html',{'data':data})


def transaction_details(request, pk):
    transaction_data=list()
    invoice_data=list()
    user = CustomUser.objects.get(username=request.user)
    business_obj = Business.objects.get(user_id_id=user)
    business_id = business_obj.business_id
    invoice_id = pk
    invoice_obj = get_object_or_404(Invoice, pk=invoice_id)
    date = invoice_obj.invoice_date
    entity_name = invoice_obj.entity_name
    amount = invoice_obj.invoice_amount
    discount = invoice_obj.applicable_discount_rate
    amount_financed = invoice_obj.invoice_total_investment
    entity_id = Entity.objects.get(entity_name=entity_name).entity_id
    roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id)
    platform_fee = roi_obj.applicable_platform_fee
    other_fee = 0
    roi = roi_obj.applicable_roi
    tenure = (invoice_obj.invoice_date + timedelta(days=roi_obj.approved_credit_period) - date.today()).days
    pdf_file = invoice_obj.invoice_pdf
    other_documents = None
    transaction_objs = Transaction.objects.filter(invoice_id_id = invoice_id)
    temp_list = list()
    temp_list.extend((invoice_id, date, entity_name, amount, discount, amount_financed, platform_fee, other_fee, roi, tenure, pdf_file, other_documents))
    invoice_data.append(temp_list)
    for i in transaction_objs:
        temp_list = list()
        transaction_id = i.transaction_id
        interest = i.settlement_amount_with_investor - i.settlement_amount_with_business
        interest = round(interest, 2)
        investment_amount = i.amount_invested
        investment_amount = round(investment_amount, 2)
        # temp_list.extend((invoice_id, transaction_id, date, entity_name, amount, discount, amount_financed, platform_fee, other_fee, roi, interest, investment_amount, tenure, pdf_file, other_documents))
        temp_list.extend((transaction_id, interest, investment_amount))
        transaction_data.append(temp_list)
        # data.append(temp_list)
    print(invoice_data)
    return render(request,'Business/transaction-details.html', {'invoice_data':invoice_data, 'transaction_data':transaction_data})


def view_details(request, mode):
    bus_id = Business.objects.get(user_id=request.user).business_id
    if mode == 0:
        invoices = Invoice.objects.filter(business_id=bus_id)
    elif mode == 1:
        invoices = Invoice.objects.filter(business_id=bus_id).filter(final_approval_status_verification='pending')
    elif mode == 2:
        invoices = Invoice.objects.filter(business_id=bus_id).filter(final_approval_status_verification='approved')
    elif mode == 3:
        invoices = Invoice.objects.filter(business_id=bus_id).filter(invoice_subscription_status__gt=0)
    elif mode == 4:
        invoices = Invoice.objects.filter(business_id=bus_id).filter(status='repaid')
    else:
        return redirect('dashboard')
    data = list()
    if len(invoices) == 0:
        temp_list = list()
        temp_list.extend(('-'*10))
        data.append(temp_list)
        message = 'No Invoices to Display'
        return render(request,'Business/view-details.html', { 'mode':mode, 'message':message})
    for i in invoices:
        temp_list = list()
        invoice_id = i.invoice_id
        entity_name = i.entity_name
        invoice_date = i.invoice_date
        invoice_amount = format_amount(i.invoice_amount)
        print(i.invoice_total_investment)
        print(i)
        if i.invoice_total_investment is None:
            invoice_total_investment = 0.0
        else:
            invoice_total_investment = format_amount(i.invoice_total_investment)
        applicable_ROI = i.applicable_ROI
        invoice_subscription_status = i.invoice_subscription_status
        invoice_due_date = i.invoice_due_date
        invoice_pdf = i.invoice_pdf
        temp_list.extend((invoice_id, entity_name, invoice_date, invoice_amount, invoice_total_investment, applicable_ROI, invoice_subscription_status, invoice_due_date, invoice_pdf))
        data.append(temp_list)
    return render(request,'Business/view-details.html', {'data' : data, 'mode':mode})


def withdrawal(request):
    bus_id = Business.objects.get(user_id=request.user).business_id
    bus_obj = Business.objects.get(business_id=bus_id)
    balance = bus_obj.escrow_balance
    bank_accounts = list()
    bank_account = bus_obj.business_bank_account_no
    bank_accounts.append(bank_account)
    if request.method == 'POST':
        account_number = request.POST['account_number']
        type_of_transaction = 'Debit'
        sub_type_of_transaction = 'withdraw'
        user_id = bus_id
        user_type = 'Business'
        user_name = bus_obj.business_name
        date_of_transaction = date.today().strftime("%Y-%m-%d")
        amount = float(request.POST['amount'])
        status = 'pending'
        balance -=  amount
        print('type_of_transaction =',type_of_transaction)
        print('user_id =',user_id)
        print('user_type =',user_type)
        print('user_name =',user_name)
        print('date_of_transaction =',date_of_transaction)
        print('amount =',amount)
        print('status =',status)
        print('account_number =',account_number)
        Escrow_acc.objects.create(type_of_transaction = type_of_transaction, sub_type_of_transaction = sub_type_of_transaction, user_id = user_id, user_type = user_type, user_name = user_name, date_of_transaction = date_of_transaction, amount = amount, status = status, balance = balance, account_number = account_number)
        bus_obj.escrow_balance = balance
        bus_obj.save()
        return redirect('withdrawal')
    balance_amount = format_amount(balance)
    return render(request, 'Business/withdrawal.html', {'bank_accounts': bank_accounts, 'balance_amount': balance_amount, 'balance':balance})
    # return render(request,'Business/withdrawal.html')

