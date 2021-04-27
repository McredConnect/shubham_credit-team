from django.shortcuts import render, redirect, get_object_or_404
from PortalLogin.models import State
from .models import *
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
import uuid
from math import ceil
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

CustomUser = get_user_model()
from MIPortal.settings import MEDIA_ROOT, MEDIA_URL


def format_amount(amount):
    amount = round(amount, 2)
    from babel.numbers import format_currency
    return format_currency(amount, 'INR', locale='en_IN')


def create_transaction(investor_obj, invested_amount, invoice_id, tenure):
    balance_inv = investor_obj.escrow_balance
    if balance_inv < invested_amount:
        message = 'Your MCred Wallet balance is low. Please add funds to continue with your investment.'
        return message
    gst_inv = 0.0
    gst_bus = 0.0
    invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
    due_date1 = invoice_obj.invoice_due_date
    tenor = (due_date1 - date.today()).days
    entity_name = invoice_obj.entity_name
    entity_obj = Entity.objects.get(entity_name=entity_name)
    business_id = invoice_obj.business_id.business_id
    business_obj = Business.objects.get(business_id=business_id)

    entity_id2 = entity_obj.entity_id
    roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
    # available_investment = invoice_obj.invoice_investment_amount
    total_investment = invoice_obj.invoice_total_investment + invested_amount

    return_amount1 = round((((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount),
                           2)
    investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1
    amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * invested_amount), 2)
    return_inv = round((amount_due1 - invested_amount), 2)
    annualized_yield = round((((return_inv / invested_amount) / tenor) * 365 * 100), 2)

    amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
    percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
    total_subs = invoice_obj.invoice_subscription_status + percentage_subs
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=investor_obj.investor_id).filter(
        entity_id=entity_id2).first()
    platform_fee_inv = invested_amount * ror_obj.applicable_platform_fee / 100 * tenor / 365
    platform_fee_bus = amt_payable_to_business * roi_obj.applicable_platform_fee / 100 * tenor / 365
    # check state
    # same_state_flag = False
    # investor_state_code = investor_obj.investor_gst_detail[:2]
    # current_state = 'Maharashtra'
    # if investor_state_code == State.objects.filter(name = current_state).first().code:
    #     same_state_flag = True
    gst_inv = platform_fee_inv * invoice_obj.applicable_gst_rate / 100
    gst_bus = platform_fee_bus * invoice_obj.applicable_gst_rate / 100
    after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
    available_investment_amount = invoice_obj.invoice_fundable_amount - (
                invoice_obj.invoice_fundable_amount * ror_obj.applicable_ror / 100 * tenure / 365)
    amount_due_on_maturity = amount_due1
    balance_bus = business_obj.escrow_balance
    type_of_transaction_inv = 'Debit'
    sub_type_of_transaction_inv = 'Deal Purchase'
    user_id_inv = investor_obj.investor_id
    user_type_inv = 'Investor'
    user_name_inv = investor_obj.investor_name
    date_of_transaction_inv = date.today().strftime("%Y-%m-%d")
    amount_inv = invested_amount + platform_fee_inv + gst_inv
    status_inv = 'approved'
    balance_inv -= amount_inv
    account_number_inv = investor_obj.investor_bank_account_no
    type_of_transaction_bus = 'Credit'
    sub_type_of_transaction_bus = 'Funding'
    user_id_bus = business_obj.business_id
    user_type_bus = 'Business'
    user_name_bus = business_obj.business_name
    date_of_transaction_bus = date.today().strftime("%Y-%m-%d")
    margin_days = roi_obj.margin_days
    print(margin_days)
    margin_retained = amount_due1 * roi_obj.applicable_roi / 100 * margin_days / 365
    amount_bus = amt_payable_to_business - platform_fee_bus - gst_bus - margin_retained
    status_bus = 'approved'
    balance_bus += amount_bus
    investor_earnings = amount_due_on_maturity - invested_amount
    account_number_bus = business_obj.business_bank_account_no
    mcred_obj = Escrow_acc.objects.filter(user_type='MCRED')
    if len(mcred_obj) == 0:
        balance_mcred = 0.0
    else:
        balance_mcred = mcred_obj.order_by('-id')[0].balance
    user_id_mcred = '1234567890'
    user_type_mcred = 'MCRED'
    user_name_mcred = 'MCRED'
    date_of_transaction_mcred = date.today().strftime("%Y-%m-%d")

    new_transaction = Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                                 invoice_upload_date=invoice_obj.invoice_upload_date,
                                                 amount_invested=invested_amount, tenor=tenor,
                                                 due_date=invoice_obj.invoice_due_date,
                                                 applicable_ROI=roi_obj.applicable_roi,
                                                 applicable_yield_investor=invoice_obj.ror_for_investor,
                                                 settlement_amount_with_investor=amount_due_on_maturity,
                                                 settlement_amount_with_business=amt_payable_to_business,
                                                 entity_id=entity_obj, business_id=business_obj,
                                                 investor_id=investor_obj, batch_no=invoice_obj.batch_no,
                                                 transaction_type='Debit', transaction_sub_type='Deal Purchase',
                                                 calculated_yield=annualized_yield,
                                                 platform_service_fee_investor=platform_fee_inv,
                                                 gst_on_platform_service_fee_investor=gst_inv,
                                                 amount_debited_from_investor_wallet=invested_amount + platform_fee_inv + gst_inv,
                                                 entity_name=entity_obj.entity_name,
                                                 gst_on_platform_service_fee_business=gst_bus,
                                                 platform_service_fee_business=platform_fee_bus,
                                                 amount_to_be_credited_in_business_wallet=amt_payable_to_business - platform_fee_bus - gst_bus - margin_retained,
                                                 status='subscribed', margin_retained=margin_retained,
                                                 business_amount_before_margin_deduct=amt_payable_to_business - platform_fee_bus - gst_bus,
                                                 investor_earnings=investor_earnings)

    Escrow_acc.objects.create(type_of_transaction=type_of_transaction_inv,
                              sub_type_of_transaction=sub_type_of_transaction_inv, user_id=user_id_inv,
                              user_type=user_type_inv, user_name=user_name_inv,
                              date_of_transaction=date_of_transaction_inv, amount=amount_inv, status=status_inv,
                              balance=balance_inv, transaction_id=new_transaction.transaction_id,
                              account_number=account_number_inv)
    investor_obj.escrow_balance = balance_inv

    Escrow_acc.objects.create(type_of_transaction=type_of_transaction_bus,
                              sub_type_of_transaction=sub_type_of_transaction_bus, user_id=user_id_bus,
                              user_type=user_type_bus, user_name=user_name_bus,
                              date_of_transaction=date_of_transaction_bus, amount=amount_bus, status=status_bus,
                              balance=balance_bus, transaction_id=new_transaction.transaction_id,
                              account_number=account_number_bus)
    business_obj.escrow_balance = balance_bus

    type_of_transaction_mcred = 'Credit'
    sub_type_of_transaction_mcred = 'Arbitrage Income'
    amount_mcred = invested_amount - amt_payable_to_business
    status_mcred = 'approved'
    balance_mcred += amount_mcred
    Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred,
                              sub_type_of_transaction=sub_type_of_transaction_mcred, user_id=user_id_mcred,
                              user_type=user_type_mcred, user_name=user_name_mcred,
                              date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred,
                              balance=balance_mcred, transaction_id=new_transaction.transaction_id)

    type_of_transaction_mcred = 'Credit '
    sub_type_of_transaction_mcred = 'Investor Fee'
    amount_mcred = platform_fee_inv + gst_inv
    status_mcred = 'approved'
    balance_mcred += amount_mcred
    Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred,
                              sub_type_of_transaction=sub_type_of_transaction_mcred, user_id=user_id_mcred,
                              user_type=user_type_mcred, user_name=user_name_mcred,
                              date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred,
                              balance=balance_mcred, transaction_id=new_transaction.transaction_id)

    type_of_transaction_mcred = 'Credit'
    sub_type_of_transaction_mcred = 'Business Fee'
    amount_mcred = platform_fee_bus + gst_bus
    status_mcred = 'approved'
    balance_mcred += amount_mcred
    Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred,
                              sub_type_of_transaction=sub_type_of_transaction_mcred, user_id=user_id_mcred,
                              user_type=user_type_mcred, user_name=user_name_mcred,
                              date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred,
                              balance=balance_mcred, transaction_id=new_transaction.transaction_id)

    type_of_transaction_mcred = 'Credit'
    sub_type_of_transaction_mcred = 'Margin Retained'
    amount_mcred = margin_retained
    status_mcred = 'approved'
    balance_mcred += amount_mcred
    Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred,
                              sub_type_of_transaction=sub_type_of_transaction_mcred, user_id=user_id_mcred,
                              user_type=user_type_mcred, user_name=user_name_mcred,
                              date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred,
                              balance=balance_mcred, transaction_id=new_transaction.transaction_id)

    invoice_obj.maturity_after_investment = after_investment_maturity
    invoice_obj.invoice_total_investment = total_investment
    invoice_obj.invoice_subscription_status = total_subs
    invoice_obj.amount_due_investor = invoice_obj.amount_due_investor + amount_due_on_maturity
    invoice_obj.save()
    business_obj.save()
    investor_obj.save()
    message = 'Thank You For Investing'
    return message


# Create your views here.
def add_funds(request):
    if request.method == 'POST':
        inv_id = Investor.objects.get(user_id=request.user).investor_id
        inv_obj = Investor.objects.get(investor_id=inv_id)
        type_of_transaction = 'Credit'
        sub_type_of_transaction = 'deposit'
        user_id = inv_id
        user_type = 'Investor'
        user_name = inv_obj.investor_name
        amount = float(request.POST['amount'])
        status = 'pending'
        mode_of_payment = request.POST['paymentmode']
        balance = inv_obj.escrow_balance
        # balance = 50000
        balance += amount
        print('type_of_transaction =', type_of_transaction)
        print('user_id =', user_id)
        print('user_type =', user_type)
        print('user_name =', user_name)
        print('amount =', amount)
        print('status =', status)
        print('mode_of_payment =', mode_of_payment)
        account_number = inv_obj.investor_bank_account_no

        Escrow_acc.objects.create(type_of_transaction=type_of_transaction,
                                  sub_type_of_transaction=sub_type_of_transaction, user_id=user_id, user_type=user_type,
                                  user_name=user_name, amount=amount, status=status, balance=balance,
                                  account_number=account_number)
        inv_obj.escrow_balance = balance
        inv_obj.save()
        message = 'Amount will be added after verification'
        # messages.success(request, message)
        return redirect('add_funds')
    return render(request, 'Investors/addfunds.html')


def change_account(request):
    if request.method == 'POST':
        bank_name = request.POST['bank_name']
        account_number = request.POST['account_number']
        ifsc_code = request.POST['ifsc_code']
        cheque = request.FILES['cheque']
        print('bank_name =', bank_name)
        print('account_number =', account_number)
        print('ifsc_code =', ifsc_code)
        print('cheque =', cheque)
        message = 'Your request for change of Primary Account has been submitted successfully'
        messages.success(request, message)
        return redirect('inv-dashboard')
    return render(request, 'Investors/change-account.html', {})


def check(request):
    if request.method == "POST":
        invested_amt = request.GET.get['invested_amt']
        print(invested_amt)
    return render(request, 'investor/investor_deals.html')


def confirmation(request):
    # invoice_obj = Invoice.objects.last()
    batch_no = request.session.get('batch_no')
    total_user_entered_amt = request.session.get('total_invoice_amount')
    entity_name = request.session.get('entity_name')
    Invoice.objects.filter(batch_no=batch_no).update(batch_invoice_amount=total_user_entered_amt)
    if request.method == 'POST':
        yesNo = request.POST['yes']
        if yesNo == 'yes':
            Invoice.objects.filter(batch_no=batch_no).update(batch_invoice_amount=total_user_entered_amt)
            return redirect('dashboard')
        elif yesNo == 'no':
            Invoice.objects.filter(batch_no=batch_no).delete()
            return redirect('home')
    return render(request, 'business/confirmation.html')


def dashboard(request):
    print(request.user)
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    entity_mapped = list()
    for i in EntityInvestorRORMapping.objects.filter(investor_id=investor_id):
        entity_obj = Entity.objects.filter(entity_id=i.entity_id.entity_id)
        for entity in entity_obj:
            entity_mapped.append(entity.entity_name)
    invoices = list()
    for i in entity_mapped:
        invoice_obj = Invoice.objects.filter(entity_name=i)
        for invoice in invoice_obj:
            invoices.append(invoice)
    transactions = Transaction.objects.filter(investor_id=investor_id)
    print('entity_mapped =', entity_mapped)
    print('invoices =', invoices)
    print('transactions =', transactions)
    current_investment = 0
    total_amount_return = 0
    total_amount_invested = 0
    total_yield = 0
    total_earning = 0
    mcred_balance = Investor.objects.get(user_id=request.user).escrow_balance
    if mcred_balance is None:
        mcred_balance = 0.0
    mcred_balance = round(mcred_balance, 2)
    pending_deals = 0
    # curr_inv_percent = 0.0
    # exp_earn_percent = 0.0
    exp_earn = 0
    completed_deals = 0
    upcoming_deals = 0
    for i in transactions:
        return_amount = i.settlement_amount_with_investor - i.amount_invested
        total_amount_invested += i.amount_invested
        total_amount_return += return_amount
        total_yield += i.calculated_yield
        if i.transaction_type == 'Debit' and i.transaction_sub_type == "Deal Purchase":
            total_earning += i.settlement_amount_with_investor - i.amount_invested
            if i.status == 'subscribed':
                invoice_due_date = i.due_date
                days = (invoice_due_date - date.today()).days
                if days < 30:
                    upcoming_deals += 1
                exp_earn += i.settlement_amount_with_investor - i.amount_invested
        if i.transaction_type == 'Debit' and i.status == 'subscribed':
            current_investment += round((i.amount_invested), 2)
            pending_deals += 1
        elif i.transaction_type == 'Debit' and i.status == 'repaid':
            completed_deals += 1
    total_earning = round(total_earning, 2)
    total_amount_return = round(total_amount_return, 2)
    exp_earn = round(exp_earn, 2)

    print('total_earning=', total_earning)
    print('total_amount_invested=', total_amount_invested)
    try:
        average_yield = round((float(total_yield) / len(transactions)), 2)
    except ZeroDivisionError:
        average_yield = 0
    joined = request.user.date_joined
    print(joined)
    try:
        curr_inv_percent = round((current_investment * 100 / (current_investment + exp_earn + mcred_balance)), 2)
    except ZeroDivisionError:
        curr_inv_percent = 0.0
    try:
        exp_earn_percent = round((exp_earn * 100 / (current_investment + exp_earn + mcred_balance)), 2)
    except ZeroDivisionError:
        exp_earn_percent = 0.0
    try:
        mcred_bal_percent = round((mcred_balance * 100 / (current_investment + exp_earn + mcred_balance)), 2)
    except:
        mcred_bal_percent = 0.0

    return render(request, 'Investors/dashboard.html',
                  {'invoices': invoices, 'total_return': total_amount_return, 'total_investment': total_amount_invested,
                   'average_yield': average_yield, 'joined': joined, 'total_earning': total_earning,
                   'current_investment': current_investment, 'mcred_balance': mcred_balance,
                   'portfolio_value': round(exp_earn + current_investment + mcred_balance, 2),
                   'pending_deals': pending_deals, 'total_deals': completed_deals + pending_deals,
                   'completed_deals': completed_deals, 'curr_inv_percent': curr_inv_percent,
                   'exp_earn_percent': exp_earn_percent, 'mcred_bal_percent': mcred_bal_percent, 'exp_earn': exp_earn,
                   'upcoming_deals': upcoming_deals})


def deal_details(request, pk):
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    invoice_obj = get_object_or_404(Invoice, pk=pk)
    # transaction = get_object_or_404(Transaction, pk=pk)
    # return_without_fee = transaction.settlement_amount_with_investor - transaction.amount_invested
    # invoice_obj = Invoice.objects.get(invoice_id = transaction.invoice_id_id)
    # entity_name = transaction.entity_name
    # tenure =  (invoice_obj.invoice_due_date - transaction.transaction_date).days
    # pdf = invoice_obj.invoice_pdf
    # gross_yield =  (return_without_fee) / transaction.amount_invested * 365 / tenure * 100
    # net_yield =  (return_without_fee - transaction.platform_service_fee_investor - transaction.gst_on_platform_service_fee_investor) / transaction.amount_invested * 365 / tenure * 100
    # gross_yield = round(gross_yield, 2)
    # net_yield = round(net_yield, 2)
    # days_left = (transaction.due_date - date.today()).days
    # repayment_date = transaction.due_date
    entity = Entity.objects.get(entity_name=invoice_obj.entity_name)
    invoice_obj.company_logo = entity.company_logo
    business = Business.objects.get(business_id=invoice_obj.business_id_id)
    # deal_expiry_date = invoice.invoice_upload_date + timedelta(days=10)
    # today = date.today()
    # deal_expiry = (deal_expiry_date - today).days
    deal_expiry = (invoice_obj.invoice_upload_date + timedelta(days=7) - date.today()).days
    return render(request, 'Investors/deal_details.html',
                  {'deal_expiry': deal_expiry, 'entity': entity, 'business': business, 'media_root': MEDIA_ROOT,
                   'media_url': MEDIA_URL, 'invoice_obj': invoice_obj})
    # return render(request, 'Investors/deal_details.html', {'invoice': invoice, 'entity': entity, 'business': business,'deal_expiry': expiry_in_days})


def investor_deals(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = list()
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    # investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit

    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        entity_ls.append(entity_name)
        invoices = Invoice.objects.filter(entity_name=entity_name).order_by()
        for j in invoices:
            j.ror_for_investor = i.applicable_ror
            tenure = (j.invoice_due_date - date.today()).days
            return_amt = round((((i.applicable_ror / 100) / 365) * tenure * j.invoice_fundable_amount), 2)
            if j.amount_due_investor is None:
                j.amount_due_investor = 0.0
            investment_amt = j.invoice_fundable_amount - j.amount_due_investor
            investment_amt = round(investment_amt - (investment_amt * i.applicable_ror / 100 * tenure / 365), 2)
            # if total amount is paid
            invested_amount = round(
                j.invoice_fundable_amount - (j.invoice_fundable_amount * i.applicable_ror / 100 * tenure / 365), 2)
            total_invest = j.invoice_total_investment
            discounted_val = (j.applicable_discount_rate / 100) * j.invoice_amount
            tenure1 = (j.invoice_due_date - j.invoice_date).days
            maturity_amount = j.invoice_amount - discounted_val
            # --> for annualized yield #
            platform_fee = invested_amount * i.applicable_platform_fee / 100 * tenure1 / 365
            gst = platform_fee * j.applicable_gst_rate / 100
            return_amount1 = round((j.invoice_fundable_amount * i.applicable_ror / 100 * tenure1 / 365), 2)
            j.expected_gross_yield = round((float(return_amount1) / float(invested_amount) / tenure1 * 365 * 100), 2)
            j.expected_net_yield = round(
                ((float(return_amount1) - platform_fee - gst) / float(invested_amount) / tenure1 * 365 * 100), 2)
            # --> end #
            j.invoice_investment_amount = investment_amt
            maturity_amount_balance = j.invoice_fundable_amount - j.amount_due_investor
            j.invoice_available_investment = round(
                maturity_amount_balance - (maturity_amount_balance * i.applicable_ror / 100 * tenure / 365), 2)
            j.maturity_after_investment = maturity_amount - j.amount_due_investor
            j.save()

    invoice_ls = []
    inactive_invoice_flag = True
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by()
        if len(invoices) > 0:
            for j in invoices:
                if inactive_invoice_flag == True and j.invoice_subscription_status < 100:
                    inactive_invoice_flag = False
                queryset = Transaction.objects.filter(investor_id=inv_id).filter(invoice_id_id=j.invoice_id)
                entity_obj = Entity.objects.get(entity_name=i)
                j.company_logo = entity_obj.company_logo
                invoice_ls.append(j)
    if len(invoice_ls) == 0:
        messages.warning(request, 'There are No Invoices to Display')
        return render(request, 'Investors/investor_deals1.html', {'today': today, 'tomorrow': tomorrow,'day_after': day_after_tom, 'empty_invoice_flag' : True})
    if inactive_invoice_flag:
        messages.warning(request, 'There are No Active Deals for Investment')
        return render(request, 'Investors/investor_deals1.html', {'today': today, 'tomorrow': tomorrow,'day_after': day_after_tom})
    entity_ls.sort()
    if request.method == 'POST':
        investor_obj = Investor.objects.get(user_id=request.user)
        invested_amount = float(request.POST['invested_amt'])
        invoice_id = request.POST['invoice_id']
        message = create_transaction(investor_obj, invested_amount, invoice_id, tenure)
        print(message, len(message))
        if len(message) > 25:
            messages.warning(request, message)
        else:
            messages.success(request, message)
        return redirect('inv-dashboard')
    return render(request, 'Investors/investor_deals1.html',
                  {'entity': entity_ls, 'data': invoice_ls, 'today': today, 'tomorrow': tomorrow,
                   'day_after': day_after_tom})


# def investor_deals(request):
#     inv_id = Investor.objects.get(user_id=request.user).investor_id
#     ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
#     entity_ls = list()
#     today = datetime.today().strftime("%d/%m/%Y")
#     tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
#     day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
#     investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit
#     for i in ror_obj:
#         entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
#         entity_ls.append(entity_name)
#         invoices = Invoice.objects.filter(entity_name=entity_name).order_by()
#         for j in invoices:
#             j.ror_for_investor = i.applicable_ror
#             tenure = (j.invoice_due_date - date.today()).days
#             return_amt = round((((i.applicable_ror / 100) / 365) * tenure * j.invoice_fundable_amount), 2)
#             investment_amt = j.invoice_fundable_amount - j.amount_due_investor
#             investment_amt = round (investment_amt - (investment_amt * i.applicable_ror / 100 * tenure / 365), 2)
#             total_invest = j.invoice_total_investment
#             discounted_val = (j.applicable_discount_rate / 100) * j.invoice_amount
#             maturity_amount = j.invoice_amount - discounted_val
#             # --> for annualized yield #
#             return_amount1 = round(
#                 (((i.applicable_ror / 100) / 365) * tenure * j.invoice_fundable_amount), 2)
#             j.expected_gross_yield = round((((float(return_amount1) / float(investment_amt)) / tenure) * 365 * 100), 2)
#             # --> end #
#             j.invoice_investment_amount = investment_amt
#             maturity_amount_balance = j.invoice_fundable_amount - j.amount_due_investor
#             j.invoice_available_investment = round(maturity_amount_balance - (maturity_amount_balance * i.applicable_ror / 100 * tenure / 365), 2)
#             j.maturity_after_investment = maturity_amount - j.amount_due_investor
#             j.save()

#     invoice_ls = []
#     for i in entity_ls:
#         invoices = Invoice.objects.filter(entity_name=i).order_by()
#         if len(invoices) > 0:
#             for j in invoices:
#                 invoice_ls.append(j)
#     entity_ls.sort()
#     if request.method == 'POST':
#         print('in if and ajax')
#         investor_obj = Investor.objects.get(user_id=request.user)
#         balance_inv = investor_obj.escrow_balance
#         invested_amount = float(request.POST['invested_amt'])
#         if balance_inv < invested_amount:
#             message = 'Your MCred Wallet balance is low. Please add funds to continue with your investment.'
#             messages.warning(request, message)
#             return redirect('inv-dashboard')
#         gst_inv = 0.0
#         gst_bus = 0.0
#         invoice_id = request.POST['invoice_id']
#         invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
#         due_date1 = invoice_obj.invoice_due_date
#         tenor = (due_date1 - date.today()).days
#         entity_name = invoice_obj.entity_name
#         business_id = invoice_obj.business_id.business_id
#         business_obj = Business.objects.get(business_id=business_id)
#         entity_obj = Entity.objects.get(entity_name=entity_name)

#         entity_id2 = entity_obj.entity_id
#         roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
#         available_investment = invoice_obj.invoice_investment_amount
#         total_investment = invoice_obj.invoice_total_investment + invested_amount

#         return_amount1 = round((((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
#         investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

#         amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * invested_amount), 2)
#         return_inv = round((amount_due1 - invested_amount), 2)

#         annualized_yield = round((((return_inv / invested_amount) / tenor) * 365 * 100), 2)

#         amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
#         percentage_subs = round(((            messages.warning(request, message)

#         investor_state_code = investor_obj.investor_gst_detail[:2]
#         current_state = 'Maharashtra'
#         if investor_state_code == State.objects.filter(name = current_state).first().code:
#             same_state_flag = True
#         gst_inv = platform_fee_inv * invoice_obj.applicable_gst_rate / 100
#         gst_bus = platform_fee_bus * invoice_obj.applicable_gst_rate / 100
#         after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
#         available_investment_amount = invoice_obj.invoice_fundable_amount - (invoice_obj.invoice_fundable_amount * ror_obj.applicable_ror / 100 * tenure / 365)
#         amount_due_on_maturity = invested_amount / available_investment_amount * invoice_obj.invoice_fundable_amount

#         print('amount_due_on_maturity=',amount_due_on_maturity)
#         print('invested_amount=',invested_amount)
#         print('available_investment_amount=',available_investment_amount)
#         print('invoice_fundable_amount=',invoice_obj.invoice_fundable_amount)
#         balance_bus = business_obj.escrow_balance
#         type_of_transaction_inv = 'Debit'
#         sub_type_of_transaction_inv = 'Deal Purchase'
#         user_id_inv = investor_obj.investor_id
#         user_type_inv = 'Investor'
#         user_name_inv = investor_obj.investor_name
#         date_of_transaction_inv = date.today().strftime("%Y-%m-%d")
#         amount_inv = invested_amount + platform_fee_inv + gst_inv
#         status_inv = 'approved'
#         balance_inv -= amount_inv
#         account_number_inv = investor_obj.investor_bank_account_no
#         type_of_transaction_bus = 'Credit'
#         sub_type_of_transaction_bus = 'Funding'
#         user_id_bus = business_obj.business_id
#         user_type_bus = 'Business'
#         user_name_bus = business_obj.business_name
#         date_of_transaction_bus = date.today().strftime("%Y-%m-%d")
#         amount_bus = amt_payable_to_business - platform_fee_bus - gst_bus
#         status_bus = 'approved'
#         balance_bus += amount_bus
#         account_number_bus = business_obj.business_bank_account_no
#         mcred_obj = Escrow_acc.objects.filter(user_type='MCRED')
#         if len(mcred_obj) == 0:
#             balance_mcred = 0.0
#         else:
#             balance_mcred = mcred_obj.order_by('-id')[0].balance
#         user_id_mcred = '1234567890'
#         user_type_mcred = 'MCRED'
#         user_name_mcred = 'MCRED'
#         date_of_transaction_mcred = date.today().strftime("%Y-%m-%d")
#         if available_investment_amount > investor_limit:
#             if invested_amount >= investor_limit:
#                 if invested_amount <= available_investment:
#                     new_transaction= Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(), invoice_upload_date=invoice_obj.invoice_upload_date, amount_invested=invested_amount, tenor=tenor, due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi, applicable_yield_investor=invoice_obj.ror_for_investor, settlement_amount_with_investor=amount_due_on_maturity, settlement_amount_with_business=amt_payable_to_business, entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj, batch_no=invoice_obj.batch_no, transaction_type='Debit', transaction_sub_type='Deal Purchase', calculated_yield=annualized_yield,  platform_service_fee_investor = platform_fee_inv, gst_on_platform_service_fee_investor = gst_inv, amount_debited_from_investor_wallet = invested_amount + platform_fee_inv + gst_inv, entity_name = entity_obj.entity_name, gst_on_platform_service_fee_business= gst_bus, platform_service_fee_business = platform_fee_bus, amount_to_be_credited_in_business_wallet = amt_payable_to_business - platform_fee_bus - gst_bus)

#                     Escrow_acc.objects.create(type_of_transaction=type_of_transaction_inv, sub_type_of_transaction = sub_type_of_transaction_inv, user_id=user_id_inv, user_type=user_type_inv, user_name=user_name_inv, date_of_transaction=date_of_transaction_inv, amount=amount_inv, status=status_inv, balance=balance_inv, transaction_id = new_transaction.transaction_id, account_number = account_number_inv)
#                     investor_obj.escrow_balance = balance_inv

#                     Escrow_acc.objects.create(type_of_transaction=type_of_transaction_bus, sub_type_of_transaction = sub_type_of_transaction_bus, user_id=user_id_bus, user_type=user_type_bus, user_name=user_name_bus, date_of_transaction=date_of_transaction_bus, amount=amount_bus, status=status_bus, balance=balance_bus, transaction_id = new_transaction.transaction_id, account_number = account_number_bus)
#                     business_obj.escrow_balance = balance_inv

#                     type_of_transaction_mcred='Credit'
#                     sub_type_of_transaction_mcred='Arbitrage Income'
#                     amount_mcred = invested_amount - amt_payable_to_business
#                     status_mcred = 'approved'
#                     balance_mcred += amount_mcred
#                     Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred, sub_type_of_transaction = sub_type_of_transaction_mcred, user_id=user_id_mcred, user_type=user_type_mcred, user_name=user_name_mcred, date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred, balance=balance_mcred, transaction_id = new_transaction.transaction_id)

#                     type_of_transaction_mcred='Credit '
#                     sub_type_of_transaction_mcred='Investor Fee'
#                     amount_mcred = platform_fee_inv + gst_inv
#                     status_mcred = 'approved'
#                     balance_mcred += amount_mcred
#                     Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred, sub_type_of_transaction = sub_type_of_transaction_mcred, user_id=user_id_mcred, user_type=user_type_mcred, user_name=user_name_mcred, date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred, balance=balance_mcred, transaction_id = new_transaction.transaction_id)

#                     type_of_transaction_mcred='Credit'
#                     sub_type_of_transaction_mcred='Business Fee'
#                     amount_mcred = platform_fee_bus + gst_bus
#                     status_mcred = 'approved'
#                     balance_mcred += amount_mcred
#                     Escrow_acc.objects.create(type_of_transaction=type_of_transaction_mcred, sub_type_of_transaction = sub_type_of_transaction_mcred, user_id=user_id_mcred, user_type=user_type_mcred, user_name=user_name_mcred, date_of_transaction=date_of_transaction_mcred, amount=amount_mcred, status=status_mcred, balance=balance_mcred, transaction_id = new_transaction.transaction_id)

#                     invoice_obj.maturity_after_investment = after_investment_maturity
#                     invoice_obj.invoice_total_investment = total_investment
#                     invoice_obj.invoice_subscription_status = total_subs
#                     invoice_obj.amount_due_investor = invoice_obj.amount_due_investor + amount_due_on_maturity
#                     invoice_obj.save()
#                     business_obj.save()
#                     investor_obj.save()
#                     message = 'Thank You For Investing'
#                     messages.success(request, message)
#                     return redirect('inv-dashboard')
#                 else:
#                     message = 'Investment amount should not be greater than available amount'
#                     messages.warning(request, message)
#                     return redirect('inv-dashboard')

#             else:
#                 message = 'Minimum investment limit is ₹ ' + str(investor_limit)
#                 messages.warning(request, message)
#                 return redirect('inv-dashboard')
#         else:
#             if invested_amount == available_investment:
#                 Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(), invoice_upload_date=invoice_obj.invoice_upload_date, amount_invested=invested_amount, tenor=tenor, due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi, applicable_yield_investor=invoice_obj.ror_for_investor, settlement_amount_with_investor=amount_due1, settlement_amount_with_business=amt_payable_to_business, entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj, batch_no=invoice_obj.batch_no, transaction_type='Debit', transaction_sub_type='Deal Purchase', calculated_yield=annualized_yield,  platform_service_fee_investor = platform_fee_inv, gst_on_platform_service_fee_investor = gst_inv, amount_debited_from_investor_wallet = invested_amount + platform_fee_inv + gst_inv, entity_name = entity_obj.entity_name, gst_on_platform_service_fee_business= gst_bus, platform_service_fee_business = platform_fee_bus, amount_to_be_credited_in_business_wallet = amt_payable_to_business - platform_fee_bus - gst_bus)
#                 Escrow_acc.objects.create(type_of_transaction=type_of_transaction_inv, user_id=user_id_inv, user_type=user_type_inv, user_name=user_name_inv, date_of_transaction=date_of_transaction_inv, amount=amount_inv, status=status_inv, balance=balance_inv)
#                 Escrow_acc.objects.create(type_of_transaction=type_of_transaction_bus, user_id=user_id_bus, user_type=user_type_bus, user_name=user_name_bus, date_of_transaction=date_of_transaction_bus, amount=amount_bus, status=status_bus, balance=balance_bus)

#                 # Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(), invoice_upload_date=invoice_obj.invoice_upload_date, amount_invested=invested_amount, tenor=tenor, due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi, applicable_yield_investor=invoice_obj.ror_for_investor, settlement_amount_with_investor=amount_due1, settlement_amount_with_business=amt_payable_to_business, entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj, batch_no=invoice_obj.batch_no, transaction_type='Debit', transaction_sub_type='Deal Purchase', calculated_yield=annualized_yield)
#                 invoice_obj.invoice_total_investment = total_investment
#                 invoice_obj.invoice_subscription_status = total_subs
#                 invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
#                 invoice_obj.save()
#                 message = 'Thank You For Investing'
#                 messages.success(request, message)
#                 return redirect('inv-dashboard')
#     return render(request, 'Investors/investor_deals.html', {'entity': entity_ls, 'data': invoice_ls, 'today': today, 'tomorrow': tomorrow, 'min_limit': investor_limit, 'day_after': day_after_tom, })


def home(request):
    today = date.today()
    business_id = Business.objects.get(user_id=request.user.id).business_id
    map_obj = EntityBusinessROIMapping.objects.filter(business_id=business_id)
    print('ror mapping=', map_obj)
    ls = []
    for i in map_obj:
        entity_name = i.entity_id.entity_name
        print('entity_name=', entity_name)
        #     entity_obj = Entity.objects.get(entity_id=entity_id)
        #     # print(entity_obj)
        #     entity_name = entity_obj.entity_name
        ls.append(entity_name)
    business_obj = Business.objects.get(user_id=request.user.id)
    face_val_discount_rate = float(business_obj.business_face_value_discount_rate)

    if request.method == "POST":
        total_invoice_amount = float(request.POST['amount'])
        entity = request.POST['entity']
        no_of_invoices = int(request.POST['invoices_no'])
        number = 0
        batch_no = get_random_string(length=6)
        for i in range(no_of_invoices):
            invoice_amount = float(request.POST["amount" + str(i)])
            invoice_date = request.POST["date" + str(i)]
            invoice_pdf = request.FILES["pdf" + str(i)]
            # face_val_discount_rate = business_obj.business_face_value_discount_rate
            discounted_val = (face_val_discount_rate / 100) * invoice_amount
            maturity_amount = invoice_amount - discounted_val
            Invoice.objects.create(invoice_amount=invoice_amount, invoice_date=invoice_date, entity_name=entity,
                                   invoice_pdf=invoice_pdf, batch_invoice_amount=total_invoice_amount,
                                   batch_number_of_invoices=no_of_invoices, batch_no=batch_no,
                                   applicable_discount_rate=face_val_discount_rate,
                                   invoice_fundable_amount=maturity_amount,
                                   business_id=Business.objects.get(user_id=request.user))
            if invoice_amount != '':
                number = number + 1
            # print(invoice_amount, invoice_pdf, invoice_date)
        batch_invoices = Invoice.objects.filter(batch_no=batch_no)
        total_user_entered_amt = 0
        for i in batch_invoices:
            total_user_entered_amt = total_user_entered_amt + i.invoice_amount
        print('total enter amt', total_user_entered_amt)
        request.session['total_invoice_amount'] = total_user_entered_amt
        request.session['batch_no'] = batch_no
        request.session['entity_name'] = entity_name
        if total_user_entered_amt > total_invoice_amount:
            messages.error(request,
                           "total invoice amount entered is more than the sum of the total amount of all invoices!"
                           "you want to update total invoice amount to " + str(total_user_entered_amt) + "Rs. ?")
            return redirect('confirmation')
        elif total_user_entered_amt < total_invoice_amount:
            messages.error(request,
                           "total invoice amount entered is less than the sum of the total amount of all invoices!"
                           "you want to update total invoice amount to " + str(total_user_entered_amt) + "Rs. ?")
            return redirect('confirmation')
        elif total_user_entered_amt == total_invoice_amount:
            messages.success(request, 'successful')
            return redirect('investor_login')
        # due_date = request.POST['due_date']
        # pdf = request.FILES['pdf']
        # business_obj = Business.objects.get(business_name='business1')
        # # entity_obj = Entity.objects.get(entity_name=entity_name)
        # # investor_obj = Investor.objects.get(investor_name=investor_name)
        # face_val_discount_rate = business_obj.business_face_value_discount_rate
        # # business_id = business_obj.business_id
        # # entity_id = entity_obj.entity_id
        # # investor_id = investor_obj.id
        # # roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id)
        # # ror_obj = EntityInvestorRORMapping.objects.get(entity_id=entity_id, investor_id=investor_id)
        # # rate_of_interest = roi_obj.applicable_roi
        # # rate_of_return = ror_obj.applicable_ror
        # # investment_date = datetime.today()
        # due_date = datetime.strptime(due_date, '%Y-%m-%d')
        # # tenure = (due_date - investment_date).days + 1
        # # print('tenure:', tenure)
        # # print('invoice amount:', invoice_amount)
        # # print('due date:', due_date)
        # # print('face value discount rate:', face_val_discount_rate)
        # # print('roi:', rate_of_interest)
        # # print('ror:', rate_of_return)
        #
        # discounted_val = face_val_discount_rate * invoice_amount
        # maturity_amount = invoice_amount - discounted_val
        # print('maturity amount:', maturity_amount)
        #
        # # income = round(((rate_of_return / 365) * tenure * maturity_amount), 2)
        # # print('income:', income)
        #
        # # investment_amount = round((maturity_amount - income), 2)
        # # print('investment_amount:', investment_amount)
        #
        # # return_to_investor = round((((income/investment_amount)/tenure) * 365), 4)
        # # print('return to investor(yield):', return_to_investor)
        #
        # # business_rate = rate_of_interest - rate_of_return
        # # business_amt = round((investment_amount - ((business_rate/365) * tenure * maturity_amount)), 2)
        # # print('business_amt:', business_amt)
        # print(pdf.name)
        # # invoice = Invoice(invoice_pdf=pdf)
        # # invoice.save()
        # Invoice.objects.create(invoice_amount=invoice_amount, invoice_due_date=due_date,
        #                        entity_name=entity_name, invoice_pdf=pdf)
        # return redirect('dashboard')
        message = 'done'
        return render(request, 'business/invoice_upload.html', {'msg': message})
    return render(request, 'business/invoice_upload.html', {'ls': ls, 'today': today.strftime("%Y-%m-%d")})


def manage_funds(request):
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    investor_obj = Investor.objects.get(user_id=request.user)
    escrow_balance = investor_obj.escrow_balance
    escrow_objs = Escrow_acc.objects.filter(user_id=investor_id).order_by('-date_of_transaction')
    withdrawal_in_progress = 0.0
    data = list()
    for i in escrow_objs:
        temp_list = list()
        amount = format_amount(i.amount)
        date_of_transaction = i.date_of_transaction
        id1 = i.id
        type_of_transaction = i.type_of_transaction
        sub_type_of_transaction = i.sub_type_of_transaction
        account_number = i.account_number
        if type_of_transaction == 'Credit':
            if i.sub_type_of_transaction == 'repayment':
                pass
            elif i.sub_type_of_transaction == 'deposit':
                sub_type_of_transaction = 'Added Funds'
                comment = f'Added from Account {str(account_number)}'

        elif type_of_transaction == 'Debit':
            if i.sub_type_of_transaction == 'Deal Purchase':
                transaction_obj = Transaction.objects.get(transaction_id=i.transaction_id)
                id1 = transaction_obj.transaction_id
                comment = f'Amount paid to Invoice {transaction_obj.invoice_id_id}'
                sub_type_of_transaction = 'Deal Purchase'
            elif i.sub_type_of_transaction == 'withdraw':
                comment = f'Withdrawal to Account {str(account_number)}'
                sub_type_of_transaction = 'Withdrawal from Wallet'
                if i.status == 'pending':
                    withdrawal_in_progress += i.amount

        temp_list.extend((date_of_transaction, id1, type_of_transaction, sub_type_of_transaction, amount, comment))
        data.append(temp_list)
    data.sort(reverse=True, key=lambda x: x[0])
    amount_available = withdrawal_in_progress + escrow_balance
    escrow_balance = round(escrow_balance, 2)
    withdrawal_in_progress = round(withdrawal_in_progress, 2)
    amount_available = round(amount_available, 2)
    print(investor_id)
    transaction_list = Transaction.objects.filter(investor_id=investor_id).order_by('-transaction_date')
    print(transaction_list)

    for t in transaction_list:
        print(t.transaction_type)
    return render(request, 'Investors/managefunds.html',
                  {'transactions': transaction_list, 'data': data, 'amount_available': amount_available,
                   'escrow_balance': escrow_balance, 'withdrawal_in_progress': withdrawal_in_progress})


def order(request, mode, sort_order):
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    gross_yield = 0.0
    net_yield = 0.0
    transaction_list = Transaction.objects.filter(investor_id=investor_id).order_by('-transaction_date')
    data = list()
    if sort_order == 0:
        flag = False
    elif sort_order == 1:
        flag = True
    else:
        return redirect('inv-dashboard')
    if mode == 0:
        index = 10
    elif mode == 1:
        index = 4
    elif mode == 2:
        index = 6
    else:
        return redirect('inv-dashboard')
    print(mode)
    for i in transaction_list:
        temp_list = list()
        transaction_id = i.transaction_id
        amount_invested = i.amount_invested
        maturity_amount = round(i.settlement_amount_with_investor, 2)
        entity_name = i.entity_name
        entity_obj = Entity.objects.get(entity_name=entity_name)
        invoice_obj = Invoice.objects.get(invoice_id=i.invoice_id_id)
        subscription_status = invoice_obj.invoice_subscription_status
        invoice_id = i.invoice_id_id
        tenure = (invoice_obj.invoice_due_date - i.transaction_date).days
        return_without_fee = i.settlement_amount_with_investor - i.amount_invested
        gross_yield = (return_without_fee) / i.amount_invested * 365 / tenure * 100
        net_yield = (
                                return_without_fee - i.platform_service_fee_investor - i.gst_on_platform_service_fee_investor) / i.amount_invested * 365 / tenure * 100
        gross_yield = round(gross_yield, 2)
        net_yield = round(net_yield, 2)
        investment_date = i.transaction_date
        fund_transfer_date = i.transaction_date
        maturity_date = i.due_date
        repayment_date = i.due_date
        days_done = (date.today() - i.transaction_date).days
        days_total = (i.due_date - i.transaction_date).days
        days_done_percent = days_done / days_total * 100
        final_percent = (days_done_percent * (67 - 31) / 100) + 31
        final_percent = ceil(final_percent) + 1
        print('days_done =', days_done)
        print('days_total =', days_total)
        print('days_done_percent =', days_done_percent)
        print('final_percent =', final_percent)
        status = i.status
        company_logo = entity_obj.company_logo
        temp_list.extend((
                         entity_name, invoice_id, transaction_id, amount_invested, maturity_amount, subscription_status,
                         gross_yield, net_yield, investment_date, fund_transfer_date, maturity_date, repayment_date,
                         final_percent, status, company_logo))
        print(temp_list)
        data.append(temp_list)
        # break
    print(data)
    data.sort(key=lambda x: x[index], reverse=flag)
    print(data)
    print('index =', index)
    print('mode =', mode)
    return render(request, 'Investors/order1.html', {'data': data, 'mode': mode, 'sort_order': sort_order})

def repayment(request):
    today = date.today()
    entities = list(Entity.objects.values_list('entity_name', flat=True).distinct())
    invoices = Invoice.objects.all()
    print(entities)
    if request.method == 'POST':
        print('in post')
        # invoice_id = request.POST['invoice_id']
        invoice_id = 'ed66647e-2f1f-464b-96e2-d1ce2b706a8a'
        invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
        invoice_date = invoice_obj.invoice_date
        total_amount = invoice_obj.invoice_amount
        # repayment_date = request.POST['repayment_date']
        # repayment_date = date.today()
        repayment_date = date(2021, 6, 13)
        due_date = invoice_obj.invoice_due_date
        entity_name = invoice_obj.entity_name
        entity_id = Entity.objects.get(entity_name=entity_name).entity_id
        business_id = invoice_obj.business_id_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id)
        credit_period = roi_obj.approved_credit_period
        lock_in_days = roi_obj.lock_in_days
        lock_in_date = invoice_date + timedelta(days=lock_in_days)
        margin_days = roi_obj.margin_days
        margin_date = due_date + timedelta(days=margin_days)
        transactions = Transaction.objects.filter(invoice_id=invoice_id)
        # Tenure is different only when lockin period is to be considered
        tenure = (repayment_date - invoice_date).days
        # Skip Flag for on time payment
        skip = False
        # Payment ON Due Date
        if repayment_date == due_date:
            skip = True
            adjustment_amount = 0.0
        # Payment BEFORE Due Date
        elif repayment_date < due_date:
            # Payment Before Lock In Period, adjust according to Lock In Period
            if repayment_date <= lock_in_date:
                tenure = lock_in_days
            # Payment After Lock In Period, adjust according to actual days
            else:
                pass
        # Payment AFTER Due Date
        else:
            # Payment WITHIN margin period
            if repayment_date <= margin_date:
                pass
            # Payment AFTER margin period
            else:
                pass
        bus_credit_amount = 0.0
        total_inv_amount = 0.0
        for i in transactions:
            inv_id = i.investor_id_id
            inv_obj = Investor.objects.get(investor_id=inv_id)
            inv_name = inv_obj.investor_name
            inv_balance = inv_obj.escrow_balance
            inv_bank_acc = inv_obj.investor_bank_account_no
            ror_obj = EntityInvestorRORMapping.objects.get(investor_id=inv_id, entity_id=entity_id)
            ror = ror_obj.applicable_ror
            inv_maturity_amount = i.settlement_amount_with_investor
            if not skip:
                change = credit_period - tenure
                adjustment_amount = inv_maturity_amount * change / 365 * ror / 100
            inv_credit_amount = inv_maturity_amount - adjustment_amount
            # Investor Escrow Entry
            # Escrow_acc.objects.create(type_of_transaction='Credit', sub_type_of_transaction = 'Repayment', user_id=inv_id, user_type='Investor', user_name=inv_name, date_of_transaction=today, amount=inv_credit_amount, status='Fully Paid', balance=inv_balance, transaction_id = i.transaction_id, account_number = inv_bank_acc)
            inv_obj.escrow_balance = inv_balance
            total_inv_amount += inv_credit_amount
            bus_credit_amount += adjustment_amount
            print('adjustment_amount', adjustment_amount)
        print('total_inv_amount', total_inv_amount)
        print('total_bus_amount', bus_credit_amount)

    return render(request, 'Investors/repayment.html', {'entities': entities, 'invoices': invoices, })


def table_view(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = list()
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        entity_ls.append(entity_name)
        invoices = Invoice.objects.filter(entity_name=entity_name).order_by()
        for j in invoices:
            j.ror_for_investor = i.applicable_ror
            tenure = (j.invoice_due_date - date.today()).days
            return_amt = round((((i.applicable_ror / 100) / 365) * tenure * j.invoice_fundable_amount), 2)
            investment_amt = j.invoice_fundable_amount - j.amount_due_investor
            investment_amt = round(investment_amt - (investment_amt * i.applicable_ror / 100 * tenure / 365), 2)
            # if total amount is paid
            invested_amount = round(
                j.invoice_fundable_amount - (j.invoice_fundable_amount * i.applicable_ror / 100 * tenure / 365), 2)
            total_invest = j.invoice_total_investment
            discounted_val = (j.applicable_discount_rate / 100) * j.invoice_amount
            tenure1 = (j.invoice_due_date - j.invoice_date).days
            maturity_amount = j.invoice_amount - discounted_val
            # --> for annualized yield #
            platform_fee = invested_amount * i.applicable_platform_fee / 100 * tenure1 / 365
            gst = platform_fee * j.applicable_gst_rate / 100
            return_amount1 = round((j.invoice_fundable_amount * i.applicable_ror / 100 * tenure1 / 365), 2)
            j.expected_gross_yield = round((float(return_amount1) / float(invested_amount) / tenure1 * 365 * 100), 2)
            j.expected_net_yield = round(
                ((float(return_amount1) - platform_fee - gst) / float(invested_amount) / tenure1 * 365 * 100), 2)
            # --> end #
            j.invoice_investment_amount = investment_amt
            maturity_amount_balance = j.invoice_fundable_amount - j.amount_due_investor
            j.invoice_available_investment = round(
                maturity_amount_balance - (maturity_amount_balance * i.applicable_ror / 100 * tenure / 365), 2)
            j.maturity_after_investment = maturity_amount - j.amount_due_investor
            j.save()

    invoice_ls = list()
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by()
        if len(invoices) > 0:
            for j in invoices:
                if inactive_invoice_flag == True and j.invoice_subscription_status < 100:
                    inactive_invoice_flag = False
                invoice_ls.append(j)
    if len(invoice_ls) == 0:
        messages.warning(request, 'There are No Invoices to Display')
        return render(request, 'Investors/table_view1.html', {'today': today, 'tomorrow': tomorrow,'day_after': day_after_tom})
    if inactive_invoice_flag:
        messages.warning(request, 'There are No Active Deals for Investment')
        return render(request, 'Investors/table_view1.html', {'today': today, 'tomorrow': tomorrow,'day_after': day_after_tom})
    entity_ls.sort()
    if request.method == 'POST':
        investor_obj = Investor.objects.get(user_id=request.user)
        invested_amount = float(request.POST['invested_amt'])
        invoice_id = request.POST['invoice_id']
        message = create_transaction(investor_obj, invested_amount, invoice_id, tenure)
        print(message, len(message))
        if len(message) > 25:
            messages.warning(request, message)
        else:
            messages.success(request, message)
        return redirect('inv-dashboard')
    for i in invoice_ls:
        i.mat_amount = i.invoice_fundable_amount - i.amount_due_investor
        i.mat_amount = format_amount(i.mat_amount)
        i.invoice_available_investment = format_amount(i.invoice_available_investment)
    return render(request, 'Investors/table_view1.html',
                  {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow,
                   'min_limit': investor_limit, 'day_after': day_after_tom})


def transactions(request):
    transaction_list = Transaction.objects.all()
    return render(request, 'test/transactions.html', {'transaction': transaction_list})


def view_details(request, mode):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    transactions = list()
    total_investment_amount = 0.0
    total_return_amount = 0.0
    total_maturity_amount = 0.0
    if mode == 0:
        all_transactions = Transaction.objects.filter(investor_id=inv_id)
    elif mode == 1:
        all_transactions = Transaction.objects.filter(investor_id=inv_id).filter(status='subscribed')
    elif mode == 2:
        all_transactions = Transaction.objects.filter(investor_id=inv_id).filter(status='repaid')
    elif mode == 3:
        all_transactions = list()
        temp_transactions = Transaction.objects.filter(investor_id=inv_id).filter(status='subscribed')
        for i in temp_transactions:
            invoice_due_date = i.due_date
            days = (invoice_due_date - date.today()).days
            if days < 30:
                all_transactions.append(i)
    else:
        return redirect('inv-dashboard')
    if len(all_transactions) == 0:
        message = 'No Transactions to Display'
        return render(request, 'Investors/view-details.html', {'mode': mode, 'message': message})

    for i in all_transactions:
        temp_list = list()
        invoice_id = i.invoice_id_id
        business_name = Business.objects.filter(business_id=i.business_id_id).first().business_name
        entity_name = i.entity_name
        invested_amount = i.amount_invested
        total_investment_amount += invested_amount
        return_amount = round(i.settlement_amount_with_investor - i.amount_invested, 2)
        total_return_amount += return_amount
        maturity_amount = round(i.settlement_amount_with_investor, 2)
        total_maturity_amount += maturity_amount
        maturity_date = i.due_date
        temp_list.extend(
            (invoice_id, business_name, entity_name, invested_amount, return_amount, maturity_amount, maturity_date))
        transactions.append(temp_list)
    total_investment_amount = round(total_investment_amount, 2)
    total_return_amount = round(total_return_amount, 2)
    total_maturity_amount = round(total_maturity_amount, 2)
    return render(request, 'Investors/view-details.html',
                  {'transactions': transactions, 'total_investment_amount': total_investment_amount,
                   'total_return_amount': total_return_amount, 'total_maturity_amount': total_maturity_amount,
                   'mode': mode})


def withdrawal(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    inv_obj = Investor.objects.get(investor_id=inv_id)
    balance = inv_obj.escrow_balance
    bank_accounts = list()
    # balance = 50000
    bank_account = inv_obj.investor_bank_account_no
    bank_accounts.append(bank_account)
    if request.method == 'POST':
        account_number = request.POST['account_number']
        type_of_transaction = 'Debit'
        sub_type_of_transaction = 'withdraw'
        user_id = inv_id
        user_type = 'Investor'
        user_name = inv_obj.investor_name
        date_of_transaction = date.today().strftime("%Y-%m-%d")
        amount = float(request.POST['amount'])
        status = 'pending'
        balance -= amount
        print('type_of_transaction =', type_of_transaction)
        print('user_id =', user_id)
        print('user_type =', user_type)
        print('user_name =', user_name)
        print('date_of_transaction =', date_of_transaction)
        print('amount =', amount)
        print('status =', status)
        print('account_number =', account_number)
        Escrow_acc.objects.create(type_of_transaction=type_of_transaction,
                                  sub_type_of_transaction=sub_type_of_transaction, user_id=user_id, user_type=user_type,
                                  user_name=user_name, date_of_transaction=date_of_transaction, amount=amount,
                                  status=status, balance=balance, account_number=account_number)
        inv_obj.escrow_balance = balance
        inv_obj.save()

        return redirect('withdraw')
    # balance_amount = format_currency(balance, 'INR', locale='en_IN')
    balance_amount = format_amount(balance)
    return render(request, 'Investors/withdrawal.html',
                  {'bank_accounts': bank_accounts, 'balance_amount': balance_amount, 'balance': balance})


# @login_required
def invoice_form(request):
    print('USER\t', request.user)

    if request.method == "POST":
        print('USER1\t', request.user)
        total_invoice_amt = request.POST['amount']
        entity = request.POST['entity_name']
        invoice_count = request.POST['invoices_no']
        batch_no = Invoice.objects.all().reverse().first().batch_no + 1
        invoice_amounts = list()
        invoice_dates = list()
        invoice_pdfs = list()
        for i in range(int(invoice_count)):
            invoice_amounts.append(float(request.POST['amount' + str(i)]))
            invoice_dates.append(request.POST['date' + str(i)])
            invoice_pdfs.append(request.FILES['pdf' + str(i)])
        for i in range(int(invoice_count)):
            Invoice.objects.create(invoice_amount=invoice_amounts[i], entity_name=entity, invoice_pdf=invoice_pdfs[i],
                                   invoice_due_date=invoice_dates[i], batch_invoice_amount=total_invoice_amt,
                                   batch_number_of_invoices=invoice_count, batch_no=batch_no)
        return render(request, 'business/invoice_upload.html', {'ls': entities})

        # for i in range(invoice_count):

        # due_date = request.POST['due_date']
        # product_code = request.POST['product_code']
        # product_desc = request.POST['product_desc']
        # invoice_no = request.POST['invoice_no']
        # invoice_date = request.POST['invoice_date']
        # eway_bill_no = request.POST['eway_bill_no']
        # goods_delivery_sts = request.POST.get('yes')
        # transporter_name = request.POST['transporter_name']
        # transporter_vehicle = request.POST['transporter_vehicle']
        # invoice_approval_sts = request.POST.get('approved')
        # invoice_assignment = request.POST.get('assignment')
        # po_date = request.POST['po_date']
        # po_number = request.POST['po_number']
        # origin_state = request.POST['origin_state']
        # delivery_state = request.POST['delivery_state']
        # tds_amount = request.POST['tds_amount']

        # if goods_delivery_sts == 'delivered_and_acknowledged':
        #     goods_delivery_date = request.POST['delivery_date']
        # else:
        #     goods_delivery_date = None

        # if invoice_approval_sts == 'approved':
        #     invoice_approval_date = request.POST['invoice_approval_date']
        # else:
        #     invoice_approval_date = None

        # if invoice_assignment == 'yes':
        #     invoice_assigned_to = request.POST['assigned_to']
        # else:
        #     invoice_assigned_to = None

        # Invoice.objects.create(goods_delivery_date=goods_delivery_date, invoice_approval_date=invoice_approval_date,
        #                        invoice_assigned_to=invoice_assigned_to, invoice_amount=total_invoice_amt,
        #                        entity_name=entity, invoice_due_date=due_date, product_HSN_code=product_code,
        #                        product_description=product_desc, invoice_number=invoice_no,
        #                        invoice_date=invoice_date, EWB_id=eway_bill_no, goods_delivery_sts=goods_delivery_sts,
        #                        transporter_name=transporter_name, transporter_vehicle_no=transporter_vehicle,
        #                        final_approval_status_verification=invoice_approval_sts,
        #                        assignment_of_invoice=invoice_assignment, PO_number=po_number, validity_of_PO=po_date,
        #                        goods_origin_state=origin_state, goods_delivery_state=delivery_state,
        #                        tds_applicable_on_invoice=tds_amount)

        # print(goods_delivery_sts, invoice_approval_sts, invoice_assignment)
    else:
        user = CustomUser.objects.filter(username=request.user).first()
        business_obj = Business.objects.filter(user_id_id=user).first()
        entities = list()
        query = EntityBusinessROIMapping.objects.filter(business_id=business_obj.business_id)
        ans = list(query.values_list('entity_id', flat=True).distinct())
        for i in ans:
            entity = Entity.objects.filter(entity_id=i).first()
            entities.append(entity.entity_name)
        # print(entities)
        # print(business_obj.business_id)
        # EntityBusinessROIMapping.objects.filter(business_id=business_id)
        return render(request, 'business/invoice_upload.html', {'ls': entities})
    # return render(request, 'forms/invoice_form.html')


# Invoice Section #


# def view_invoice(request, pk):
#     invoice = get_object_or_404(Invoice, pk=pk)
#     invoice_amt = float(invoice.invoice_amount)
#     maturity_amt = float(invoice.invoice_fundable_amount)
#     due_date = invoice.invoice_due_date
#     # discount_rate = invoice.applicable_discount_rate
#     # entity details:
#     entity_name = invoice.entity_name
#     entity_obj = Entity.objects.get(entity_name=entity_name)
#     entity_id = entity_obj.entity_id
#
#     business_name = invoice.business_name
#     business_obj = Business.objects.get(business_name=business_name)
#     business_id = business_obj.business_id
#     if request.method == "POST":
#         investor_name = request.POST['investor_name']
#         invested_amt = float(request.POST['invested_amt'])
#         investor_obj = Investor.objects.get(investor_name=investor_name)
#         investor_id = investor_obj.id
#         roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id)
#         ror_obj = EntityInvestorRORMapping.objects.get(entity_id=entity_id, investor_id=investor_id)
#         rate_of_interest = roi_obj.applicable_roi
#         rate_of_return = ror_obj.applicable_ror
#         transaction_date = date.today()
#         tenure = (due_date-transaction_date).days
#         print(maturity_amt)
#
#         return_amt = round(((rate_of_return / 365) * tenure * maturity_amt), 2)
#         print(return_amt)
#         investment_amt = round((maturity_amt - return_amt), 2)
#         print('investment_amt', investment_amt)
#
#         amount_due = round(((maturity_amt/investment_amt) * invested_amt), 2)
#         print(amount_due)
#
#         return_inv = amount_due - invested_amt
#         print(return_inv)
#
#         annualized_yield = round((((return_inv / invested_amt) / tenure) * 365*100), 2)
#         print(annualized_yield)
#
#         amt_payable_to_business = round(amount_due - ((rate_of_interest/365) * tenure * amount_due), 2)
#         print(amt_payable_to_business)
#
#         percentage_subs = round(((amount_due/maturity_amt) * 100), 2)
#         print(percentage_subs)
#
#         total_subs = invoice.invoice_subscription_status + percentage_subs
#         total_investment = invoice.invoice_total_investment
#
#         if total_subs < 100:
#             Transaction.objects.create(invoice_id=invoice.id, transaction_date=transaction_date,
#                                        invoice_upload_date=invoice.invoice_upload_date, amount_invested=invested_amt, tenor=tenure,
#                                        due_date=due_date, applicable_ROI=rate_of_interest,
#                                        applicable_yield_investor=rate_of_return,
#                                        amount_settled_with_business=amt_payable_to_business, business_id=business_id,
#                                        investor_id=investor_id, entity_id=entity_id,
#                                        settlement_amount_with_investor=amount_due)
#             invoice.invoice_total_investment = total_investment + invested_amt
#             invoice.invoice_investment_amount = investment_amt - invoice.invoice_total_investment
#             invoice.invoice_subscription_status = total_subs
#             invoice.save()
#     a decision on display of    else:
#             messages.error(request, 'Amount exceeds!')
#
#         #
#         # if investment_amt < float(invested_amt):
#         #     messages.error(request, "Sorry, cannot invest more than available investment amount.")
#         #     # return redirect(view_invoice(request))
#         #
#         # if invested_amt <= float(invoice.invoice_investment_amount):
#         #     Transaction.objects.create(invoice_id=invoice.id, transaction_date=transaction_date,
#         #                                invoice_upload_date=invoice.invoice_upload_date, amount_invested=invested_amt, tenor=tenure,
#         #                                due_date=due_date, applicable_ROI=rate_of_interest,
#         #                                applicable_yield_investor=rate_of_return,
#         #                                amount_settled_with_business=amt_payable_to_business, business_id=business_id,
#         #                                investor_id=investor_id, entity_id=entity_id,
#         #                                settlement_amount_with_investor=amount_due)
#         #
#         #     # available_investment_amt = investment_amt - total_investment
#         #     invoice.invoice_total_investment = total_investment + invested_amt
#         #     invoice.invoice_investment_amount = investment_amt - invoice.invoice_total_investment
#         #     invoice.save()
#         # investment_amt = investment_amt - invoice.invoice_total_investment
#         return render(request, 'result.html', {'invoice_amt': invoice_amt, 'maturity_amt': maturity_amt,
#                                                'available_investment_amt': round((investment_amt - invoice.invoice_total_investment), 2),
#                                                'due_date': due_date})
#     return render(request, 'result.html', {'invoice_amt': invoice_amt, 'maturity_amt': maturity_amt,
#                                            'available_investment_amt': round((invoice.invoice_investment_amount), 2),
#                                            'due_date': due_date})


def viewInvoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    total_invoice_amount = invoice.invoice_amount
    entity = invoice.entity_name
    due_date = invoice.invoice_due_date
    pdf_name = invoice.invoice_pdf
    business_obj = Business.objects.get(business_id=invoice.business_id)
    face_val_discount_rate = business_obj.business_face_value_discount_rate
    print(total_invoice_amount, entity, due_date, pdf_name.url, date.today())
    discounted_val = (face_val_discount_rate / 100) * total_invoice_amount
    maturity_amount = total_invoice_amount - discounted_val
    invoice.invoice_fundable_amount = maturity_amount
    invoice.save()
    if request.method == "POST":
        investor_id = request.POST['id']
        invested_amt = float(request.POST['invested_amt'])
        entity_obj = Entity.objects.get(entity_name=invoice.entity_name)
        print(entity_obj)
        entity_id = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=invoice.business_id, entity_id=entity_id)
        rate_of_interest = roi_obj.applicable_roi
        ror_obj = EntityInvestorRORMapping.objects.get(entity_id=entity_id, investor_id=investor_id)
        rate_of_return = ror_obj.applicable_ror
        transaction_date = date.today()
        # due_date = datetime.strptime(due_date, '%Y-%m-%d')
        tenure = (due_date - transaction_date).days
        # tenure = 72

        return_amt = round((((rate_of_return / 100) / 365) * tenure * maturity_amount), 2)
        print(return_amt)
        investment_amt = round((maturity_amount - return_amt), 2)
        print('investment_amt', investment_amt)

        amount_due = round(((maturity_amount / investment_amt) * invested_amt), 2)
        print(amount_due)

        return_inv = amount_due - invested_amt
        print(return_inv)

        annualized_yield = round((((return_inv / invested_amt) / tenure) * 365 * 100), 2)
        print(annualized_yield)

        amt_payable_to_business = round(amount_due - (((rate_of_interest / 100) / 365) * tenure * amount_due), 2)
        print(amt_payable_to_business)

        percentage_subs = round(((amount_due / maturity_amount) * 100), 2)
        print(percentage_subs)

        total_subs = invoice.invoice_subscription_status + percentage_subs
        total_investment = invoice.invoice_total_investment

        context = {'investment_done': invested_amt, 'amount_due': amount_due, 'return': return_inv,
                   'annualized_yield': annualized_yield, 'amount_payable': amt_payable_to_business}
        if total_subs <= 100:
            Transaction.objects.create(invoice_id=invoice.id, transaction_date=transaction_date,
                                       invoice_upload_date=invoice.invoice_upload_date, amount_invested=invested_amt,
                                       tenor=tenure,
                                       due_date=due_date, applicable_ROI=rate_of_interest,
                                       applicable_yield_investor=rate_of_return,
                                       amount_settled_with_business=amt_payable_to_business,
                                       business_id=invoice.business_id,
                                       investor_id=investor_id, entity_id=entity_id,
                                       settlement_amount_with_investor=amount_due)
            invoice.invoice_total_investment = total_investment + invested_amt
            invoice.invoice_investment_amount = round((investment_amt - invoice.invoice_total_investment), 2)
            invoice.invoice_subscription_status = total_subs
            invoice.save()
            return redirect('transactions')
        else:
            messages.error(request, 'Amount exceeds!')
            return redirect('dashboard')
        # return render(request, 'result.html', {'invoice_amt': total_invoice_amount, 'maturity_amt': maturity_amount,
        #                                        'available_investment_amt': invoice.invoice_investment_amount,
        #                                        'due_date': due_date}, context)
    return render(request, 'viewInvoice.html', {'total_invoice_amount': total_invoice_amount,
                                                'entity': entity, 'due_date': due_date, 'pdf_name': pdf_name.url,
                                                'available_investment_amt': invoice.invoice_investment_amount,
                                                'maturity_amount': maturity_amount})


# We can delete this:
def invoice_detail(request):
    return render(request, 'business/invoice_detail.html')


def sort_maturity(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('invoice_due_date')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices[0])
    entity_ls.sort()
    # print(invoice_ls)
    if request.method == 'POST' and request.is_ajax():
        invested_amount = request.POST['amt']
        # print(invested_amount)
        invoice_id = request.POST['invoice_id']
        investor_id = Investor.objects.get(user_id=request.user).investor_id
        # print('investor_id=', investor_id)
        invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
        # print('invoice_obj=', invoice_obj)
        due_date1 = invoice_obj.invoice_due_date
        tenor = (due_date1 - date.today()).days
        entity_name = invoice_obj.entity_name
        business_id = invoice_obj.business_id.business_id
        business_obj = Business.objects.get(business_id=business_id)
        # print('business_obj=', business_obj)
        entity_obj = Entity.objects.get(entity_name=entity_name)
        investor_obj = Investor.objects.get(user_id=request.user)
        # print('investor_obj=', investor_obj)
        entity_id2 = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
        # print('roi_obj=', roi_obj)
        available_investment = round((invoice_obj.invoice_investment_amount - invoice_obj.invoice_total_investment), 2)
        total_investment = invoice_obj.invoice_total_investment + float(invested_amount)

        # if invested_amt1 < investor_limit:
        return_amount1 = round(
            (((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
        investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

        amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * float(invested_amount)), 2)
        # print(amount_due1, i.maturity_after_investment)
        return_inv = round((amount_due1 - float(invested_amount)), 2)

        annualized_yield = round((((return_inv / float(invested_amount)) / tenor) * 365 * 100), 2)

        amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
        # print(amt_payable_to_business)

        percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
        total_subs = invoice_obj.invoice_subscription_status + percentage_subs

        after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
        print(after_investment_maturity)
        if available_investment > investor_limit:
            # print(investor_limit, invested_amt1)
            if float(invested_amount) >= investor_limit:
                if float(invested_amount) <= available_investment:
                    Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                               invoice_upload_date=invoice_obj.invoice_upload_date,
                                               amount_invested=float(invested_amount),
                                               tenor=tenor,
                                               due_date=invoice_obj.invoice_due_date,
                                               applicable_ROI=roi_obj.applicable_roi,
                                               applicable_yield_investor=invoice_obj.ror_for_investor,
                                               settlement_amount_with_investor=amount_due1,
                                               settlement_amount_with_business=amt_payable_to_business,
                                               entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                               batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                               transaction_sub_type='Deal Purchase',
                                               calculated_yield=annualized_yield)
                    # obj = Invoice(id=invoice_id)
                    invoice_obj.maturity_after_investment = after_investment_maturity
                    invoice_obj.invoice_total_investment = total_investment
                    invoice_obj.invoice_subscription_status = total_subs
                    invoice_obj.amount_due_investor = invoice_obj.amount_due_investor + amount_due1
                    # print('maturity_after:', invoice_obj1.invoice_fundable_amount-amount_due1)
                    invoice_obj.save()
                    message = 'thank you for investing.'
                    return JsonResponse({'msg': message})
                else:
                    message = 'Investment amount should not be greater than available amount.'
                    return JsonResponse({'msg': message})
            else:
                message = 'Minimum investment limit is Rs. ' + str(investor_limit)
                return JsonResponse({'msg': message})
        else:
            if float(invested_amount) == available_investment:
                Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                           invoice_upload_date=invoice_obj.invoice_upload_date,
                                           amount_invested=invested_amount,
                                           tenor=tenor,
                                           due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                           applicable_yield_investor=invoice_obj.ror_for_investor,
                                           settlement_amount_with_investor=amount_due1,
                                           settlement_amount_with_business=amt_payable_to_business,
                                           entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                           batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                           transaction_sub_type='Deal Purchase',
                                           calculated_yield=annualized_yield)
                invoice_obj.invoice_total_investment = total_investment
                invoice_obj.invoice_subscription_status = total_subs
                invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
                invoice_obj.save()
                message = 'thank you for investing1.'
            return JsonResponse({'msg': message})
            # print(available_investment, invested_amt1)
            message = 'investment amount should be equal to the available amount.'
            return JsonResponse({'msg': message})
    return render(request, 'Investors/sort/sort_maturity.html',
                  {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow,
                   'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_funded(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('invoice_subscription_status')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices[0])
    entity_ls.sort()
    if request.method == 'POST' and request.is_ajax():
        invested_amount = request.POST['amt']
        # print(invested_amount)
        invoice_id = request.POST['invoice_id']
        investor_id = Investor.objects.get(user_id=request.user).investor_id
        # print('investor_id=', investor_id)
        invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
        # print('invoice_obj=', invoice_obj)
        due_date1 = invoice_obj.invoice_due_date
        tenor = (due_date1 - date.today()).days
        entity_name = invoice_obj.entity_name
        business_id = invoice_obj.business_id.business_id
        business_obj = Business.objects.get(business_id=business_id)
        # print('business_obj=', business_obj)
        entity_obj = Entity.objects.get(entity_name=entity_name)
        investor_obj = Investor.objects.get(user_id=request.user)
        # print('investor_obj=', investor_obj)
        entity_id2 = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
        # print('roi_obj=', roi_obj)
        available_investment = round((invoice_obj.invoice_investment_amount - invoice_obj.invoice_total_investment), 2)
        total_investment = invoice_obj.invoice_total_investment + float(invested_amount)

        # if invested_amt1 < investor_limit:
        return_amount1 = round(
            (((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
        investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

        amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * float(invested_amount)), 2)
        # print(amount_due1, i.maturity_after_investment)
        return_inv = round((amount_due1 - float(invested_amount)), 2)

        annualized_yield = round((((return_inv / float(invested_amount)) / tenor) * 365 * 100), 2)

        amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
        # print(amt_payable_to_business)

        percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
        total_subs = invoice_obj.invoice_subscription_status + percentage_subs

        after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
        print(after_investment_maturity)
        if available_investment > investor_limit:
            # print(investor_limit, invested_amt1)
            if float(invested_amount) >= investor_limit:
                if float(invested_amount) <= available_investment:
                    Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                               invoice_upload_date=invoice_obj.invoice_upload_date,
                                               amount_invested=float(invested_amount),
                                               tenor=tenor,
                                               due_date=invoice_obj.invoice_due_date,
                                               applicable_ROI=roi_obj.applicable_roi,
                                               applicable_yield_investor=invoice_obj.ror_for_investor,
                                               settlement_amount_with_investor=amount_due1,
                                               settlement_amount_with_business=amt_payable_to_business,
                                               entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                               batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                               transaction_sub_type='Deal Purchase',
                                               calculated_yield=annualized_yield)
                    # obj = Invoice(id=invoice_id)
                    invoice_obj.maturity_after_investment = after_investment_maturity
                    invoice_obj.invoice_total_investment = total_investment
                    invoice_obj.invoice_subscription_status = total_subs
                    invoice_obj.amount_due_investor = invoice_obj.amount_due_investor + amount_due1
                    # print('maturity_after:', invoice_obj1.invoice_fundable_amount-amount_due1)
                    invoice_obj.save()
                    message = 'thank you for investing.'
                    return JsonResponse({'msg': message})
                else:
                    message = 'Investment amount should not be greater than available amount.'
                    return JsonResponse({'msg': message})
            else:
                message = 'Minimum investment limit is Rs. ' + str(investor_limit)
                return JsonResponse({'msg': message})
        else:
            if float(invested_amount) == available_investment:
                Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                           invoice_upload_date=invoice_obj.invoice_upload_date,
                                           amount_invested=invested_amount,
                                           tenor=tenor,
                                           due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                           applicable_yield_investor=invoice_obj.ror_for_investor,
                                           settlement_amount_with_investor=amount_due1,
                                           settlement_amount_with_business=amt_payable_to_business,
                                           entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                           batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                           transaction_sub_type='Deal Purchase',
                                           calculated_yield=annualized_yield)
                invoice_obj.invoice_total_investment = total_investment
                invoice_obj.invoice_subscription_status = total_subs
                invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
                invoice_obj.save()
                message = 'thank you for investing1.'
            return JsonResponse({'msg': message})
            # print(available_investment, invested_amt1)
            message = 'investment amount should be equal to the available amount.'
            return JsonResponse({'msg': message})
    return render(request, 'Investors/sort/sort_funded.html',
                  {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow,
                   'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_available_investment(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('invoice_available_investment')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices[0])
    entity_ls.sort()
    invoice_ls = invoice_ls[::-1]
    # invoice_ls = invoice_ls[::-1]
    if request.method == 'POST' and request.is_ajax():
        invested_amount = request.POST['amt']
        # print(invested_amount)
        invoice_id = request.POST['invoice_id']
        investor_id = Investor.objects.get(user_id=request.user).investor_id
        # print('investor_id=', investor_id)
        invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
        # print('invoice_obj=', invoice_obj)
        due_date1 = invoice_obj.invoice_due_date
        tenor = (due_date1 - date.today()).days
        entity_name = invoice_obj.entity_name
        business_id = invoice_obj.business_id.business_id
        business_obj = Business.objects.get(business_id=business_id)
        # print('business_obj=', business_obj)
        entity_obj = Entity.objects.get(entity_name=entity_name)
        investor_obj = Investor.objects.get(user_id=request.user)
        # print('investor_obj=', investor_obj)
        entity_id2 = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
        # print('roi_obj=', roi_obj)
        available_investment = round((invoice_obj.invoice_investment_amount - invoice_obj.invoice_total_investment), 2)
        total_investment = invoice_obj.invoice_total_investment + float(invested_amount)

        # if invested_amt1 < investor_limit:
        return_amount1 = round(
            (((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
        investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

        amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * float(invested_amount)), 2)
        # print(amount_due1, i.maturity_after_investment)
        return_inv = round((amount_due1 - float(invested_amount)), 2)

        annualized_yield = round((((return_inv / float(invested_amount)) / tenor) * 365 * 100), 2)

        amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
        # print(amt_payable_to_business)

        percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
        total_subs = invoice_obj.invoice_subscription_status + percentage_subs

        after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
        print(after_investment_maturity)
        if available_investment > investor_limit:
            # print(investor_limit, invested_amt1)
            if float(invested_amount) >= investor_limit:
                if float(invested_amount) <= available_investment:
                    Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                               invoice_upload_date=invoice_obj.invoice_upload_date,
                                               amount_invested=float(invested_amount),
                                               tenor=tenor,
                                               due_date=invoice_obj.invoice_due_date,
                                               applicable_ROI=roi_obj.applicable_roi,
                                               applicable_yield_investor=invoice_obj.ror_for_investor,
                                               settlement_amount_with_investor=amount_due1,
                                               settlement_amount_with_business=amt_payable_to_business,
                                               entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                               batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                               transaction_sub_type='Deal Purchase',
                                               calculated_yield=annualized_yield)
                    # obj = Invoice(id=invoice_id)
                    invoice_obj.maturity_after_investment = after_investment_maturity
                    invoice_obj.invoice_total_investment = total_investment
                    invoice_obj.invoice_subscription_status = total_subs
                    invoice_obj.amount_due_investor = invoice_obj.amount_due_investor + amount_due1
                    # print('maturity_after:', invoice_obj1.invoice_fundable_amount-amount_due1)
                    invoice_obj.save()
                    message = 'thank you for investing.'
                    return JsonResponse({'msg': message})
                else:
                    message = 'Investment amount should not be greater than available amount.'
                    return JsonResponse({'msg': message})
            else:
                message = 'Minimum investment limit is Rs. ' + str(investor_limit)
                return JsonResponse({'msg': message})
        else:
            if float(invested_amount) == available_investment:
                Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                           invoice_upload_date=invoice_obj.invoice_upload_date,
                                           amount_invested=invested_amount,
                                           tenor=tenor,
                                           due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                           applicable_yield_investor=invoice_obj.ror_for_investor,
                                           settlement_amount_with_investor=amount_due1,
                                           settlement_amount_with_business=amt_payable_to_business,
                                           entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                           batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                           transaction_sub_type='Deal Purchase',
                                           calculated_yield=annualized_yield)
                invoice_obj.invoice_total_investment = total_investment
                invoice_obj.invoice_subscription_status = total_subs
                invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
                invoice_obj.save()
                message = 'thank you for investing1.'
            return JsonResponse({'msg': message})
            # print(available_investment, invested_amt1)
            message = 'investment amount should be equal to the available amount.'
            return JsonResponse({'msg': message})
    return render(request, 'Investors/sort/sort_available_investment.html',
                  {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow,
                   'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_yield(request):
    inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(user_id=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('ror_for_investor')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices[0])
    entity_ls.sort()
    # invoice_ls = invoice_ls[::-1]
    if request.method == 'POST' and request.is_ajax():
        invested_amount = request.POST['amt']
        # print(invested_amount)
        invoice_id = request.POST['invoice_id']
        investor_id = Investor.objects.get(user_id=request.user).investor_id
        # print('investor_id=', investor_id)
        invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
        # print('invoice_obj=', invoice_obj)
        due_date1 = invoice_obj.invoice_due_date
        tenor = (due_date1 - date.today()).days
        entity_name = invoice_obj.entity_name
        business_id = invoice_obj.business_id.business_id
        business_obj = Business.objects.get(business_id=business_id)
        # print('business_obj=', business_obj)
        entity_obj = Entity.objects.get(entity_name=entity_name)
        investor_obj = Investor.objects.get(user_id=request.user)
        # print('investor_obj=', investor_obj)
        entity_id2 = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
        # print('roi_obj=', roi_obj)
        available_investment = round((invoice_obj.invoice_investment_amount - invoice_obj.invoice_total_investment), 2)
        total_investment = invoice_obj.invoice_total_investment + float(invested_amount)

        # if invested_amt1 < investor_limit:
        return_amount1 = round(
            (((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
        investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

        amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * float(invested_amount)), 2)
        # print(amount_due1, i.maturity_after_investment)
        return_inv = round((amount_due1 - float(invested_amount)), 2)

        annualized_yield = round((((return_inv / float(invested_amount)) / tenor) * 365 * 100), 2)

        amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
        # print(amt_payable_to_business)

        percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
        total_subs = invoice_obj.invoice_subscription_status + percentage_subs

        after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
        print(after_investment_maturity)
        if available_investment > investor_limit:
            # print(investor_limit, invested_amt1)
            if float(invested_amount) >= investor_limit:
                if float(invested_amount) <= available_investment:
                    Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                               invoice_upload_date=invoice_obj.invoice_upload_date,
                                               amount_invested=float(invested_amount),
                                               tenor=tenor,
                                               due_date=invoice_obj.invoice_due_date,
                                               applicable_ROI=roi_obj.applicable_roi,
                                               applicable_yield_investor=invoice_obj.ror_for_investor,
                                               settlement_amount_with_investor=amount_due1,
                                               settlement_amount_with_business=amt_payable_to_business,
                                               entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                               batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                               transaction_sub_type='Deal Purchase',
                                               calculated_yield=annualized_yield)
                    # obj = Invoice(id=invoice_id)
                    invoice_obj.maturity_after_investment = after_investment_maturity
                    invoice_obj.invoice_total_investment = total_investment
                    invoice_obj.invoice_subscription_status = total_subs
                    invoice_obj.amount_due_investor = invoice_obj.amount_due_investor + amount_due1
                    # print('maturity_after:', invoice_obj1.invoice_fundable_amount-amount_due1)
                    invoice_obj.save()
                    message = 'thank you for investing.'
                    return JsonResponse({'msg': message})
                else:
                    message = 'Investment amount should not be greater than available amount.'
                    return JsonResponse({'msg': message})
            else:
                message = 'Minimum investment limit is Rs. ' + str(investor_limit)
                return JsonResponse({'msg': message})
        else:
            if float(invested_amount) == available_investment:
                Transaction.objects.create(invoice_id=invoice_obj, transaction_date=date.today(),
                                           invoice_upload_date=invoice_obj.invoice_upload_date,
                                           amount_invested=invested_amount,
                                           tenor=tenor,
                                           due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                           applicable_yield_investor=invoice_obj.ror_for_investor,
                                           settlement_amount_with_investor=amount_due1,
                                           settlement_amount_with_business=amt_payable_to_business,
                                           entity_id=entity_obj, business_id=business_obj, investor_id=investor_obj,
                                           batch_no=invoice_obj.batch_no, transaction_type='Debit',
                                           transaction_sub_type='Deal Purchase',
                                           calculated_yield=annualized_yield)
                invoice_obj.invoice_total_investment = total_investment
                invoice_obj.invoice_subscription_status = total_subs
                invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
                invoice_obj.save()
                message = 'thank you for investing1.'
            return JsonResponse({'msg': message})
            # print(available_investment, invested_amt1)
            message = 'investment amount should be equal to the available amount.'
            return JsonResponse({'msg': message})
    return render(request, 'Investors/sort/sort_yield.html',
                  {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow,
                   'min_limit': investor_limit, 'day_after': day_after_tom})


def help(request):
    data = QuestionAnswer.objects.filter(user_type='investor')
    return render(request, 'Investors/help.html', {'data': data})


def view_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return_inv = round((transaction.settlement_amount_with_investor - transaction.amount_invested), 2)
    return render(request, 'test/view_transaction.html', {'transaction': transaction, 'return': return_inv})


# Temp inv login , can be delete later:
def investor_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['pwd']
        # user = CustomUser(username=name)
        # user.set_password(password)
        # user.save()
        # investor_id = uuid.uuid4()
        # Business.objects.create(business_id=business_id, business_name=user.username, user_id=user)
        # Investor.objects.create(investor_id=investor_id, investor_name=user.username, user_id=user)

        user = authenticate(username=name, password=password)
        print(user)
        if user is not None:
            if user.type == 'investor':
                auth.login(request, user)
                return redirect('investor_deals')
            else:
                messages.error(request, 'Only for investor.')
                return redirect('investor_login')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('investor_login')
    return render(request, 'test/inv_login.html')


# Temp Business login, can be delete later:
def business_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['pwd']
        user = authenticate(username=name, password=password)
        print(user)
        if user is not None:
            if user.type == 'business':
                auth.login(request, user)
                return render(request, 'Business/dashboard.html')
            else:
                messages.error(request, 'Only for investor.')
                return redirect('business_login')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('business_login')
    return render(request, 'business/business_login.html')


def refer_and_earn(request):
    return render(request, 'Investors/refer-and-earn.html')


def update_invoice(request):
    # inv_id = Investor.objects.get(user_id=request.user).investor_id
    ror_objs = EntityBusinessROIMapping.objects.all()
    for i in ror_objs:
        entity_name = Entity.objects.get(entity_id=i.entity_id.entity_id).entity_name
        invoices = Invoice.objects.filter(entity_name=entity_name).order_by()
        for j in invoices:
            credit_period = i.approved_credit_period
            j.invoice_due_date = j.invoice_date + timedelta(days=credit_period)
            j.save()
    transactions = Transaction.objects.all()
    for i in transactions:
        invoice_obj = Invoice.objects.get(invoice_id=i.invoice_id_id)
        i.due_date = invoice_obj.invoice_due_date
        i.save()
    return redirect('inv-dashboard')