from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import *

# Create your views here.


def invoice_form(request):
    if request.method == "POST":
        total_invoice_amt = request.POST['amount']
        entity = request.POST['entity_name']
        due_date = request.POST['due_date']
        product_code = request.POST['product_code']
        product_desc = request.POST['product_desc']
        invoice_no = request.POST['invoice_no']
        invoice_date = request.POST['invoice_date']
        eway_bill_no = request.POST['eway_bill_no']
        goods_delivery_sts = request.POST.get('yes')
        transporter_name = request.POST['transporter_name']
        transporter_vehicle = request.POST['transporter_vehicle']
        invoice_approval_sts = request.POST.get('approved')
        invoice_assignment = request.POST.get('assignment')
        po_date = request.POST['po_date']
        po_number = request.POST['po_number']
        origin_state = request.POST['origin_state']
        delivery_state = request.POST['delivery_state']
        tds_amount = request.POST['tds_amount']

        if goods_delivery_sts == 'delivered_and_acknowledged':
            goods_delivery_date = request.POST['delivery_date']
        else:
            goods_delivery_date = None

        if invoice_approval_sts == 'approved':
            invoice_approval_date = request.POST['invoice_approval_date']
        else:
            invoice_approval_date = None

        if invoice_assignment == 'yes':
            invoice_assigned_to = request.POST['assigned_to']
        else:
            invoice_assigned_to = None

        Invoice.objects.create(goods_delivery_date=goods_delivery_date, invoice_approval_date=invoice_approval_date,
                               invoice_assigned_to=invoice_assigned_to, invoice_amount=total_invoice_amt,
                               entity_name=entity, invoice_due_date=due_date, product_HSN_code=product_code,
                               product_description=product_desc, invoice_number=invoice_no,
                               invoice_date=invoice_date, EWB_id=eway_bill_no, goods_delivery_sts=goods_delivery_sts,
                               transporter_name=transporter_name, transporter_vehicle_no=transporter_vehicle,
                               final_approval_status_verification=invoice_approval_sts,
                               assignment_of_invoice=invoice_assignment, PO_number=po_number, validity_of_PO=po_date,
                               goods_origin_state=origin_state, goods_delivery_state=delivery_state,
                               tds_applicable_on_invoice=tds_amount)

        print(goods_delivery_sts, invoice_approval_sts, invoice_assignment)
    return render(request, 'business/invoice_upload.html')
    # return render(request, 'forms/invoice_form.html')

# Invoice Section #


def home(request):
    today = date.today()
    business_id = Business.objects.get(user_id=request.user).business_id
    map_obj = EntityBusinessROIMapping.objects.filter(business_id=business_id)
    # print(map_obj)
    ls = []
    for i in map_obj:
        entity_id = i.entity_id.entity_id
        # print(entity_id)
        entity_obj = Entity.objects.get(entity_id=entity_id)
        # print(entity_obj)
        entity_name = entity_obj.entity_name
        ls.append(entity_name)
    # print(ls)
    business_obj = Business.objects.get(user_id=request.user)
    face_val_discount_rate = float(business_obj.business_face_value_discount_rate)
    # print(face_val_discount_rate)
    # entity_name = Entity.objects.get
    if request.method == "POST":
        total_invoice_amount = float(request.POST['amount'])
        entity = request.POST['entity']
        no_of_invoices = int(request.POST['invoices_no'])
        number = 0
        batch_no = get_random_string(length=6)
        for i in range(no_of_invoices):
            invoice_amount = float(request.POST["amount"+str(i)])
            invoice_date = request.POST["date"+str(i)]
            invoice_pdf = request.FILES["pdf"+str(i)]
            face_val_discount_rate = business_obj.business_face_value_discount_rate
            discounted_val = (face_val_discount_rate / 100) * invoice_amount
            maturity_amount = invoice_amount - discounted_val
            Invoice.objects.create(invoice_amount=invoice_amount, invoice_date=invoice_date, entity_name=entity,
                                   invoice_pdf=invoice_pdf, batch_invoice_amount=total_invoice_amount,
                                   batch_number_of_invoices=no_of_invoices, batch_no=batch_no,
                                   applicable_discount_rate=face_val_discount_rate, invoice_fundable_amount=maturity_amount,
                                   business_id=business_id)
            if invoice_amount != '':
                number = number + 1
            print(invoice_amount, invoice_pdf, invoice_date)
        batch_invoices = Invoice.objects.filter(batch_no=batch_no)
        total_user_entered_amt = 0
        for i in batch_invoices:
            total_user_entered_amt = total_user_entered_amt + i.invoice_amount
        print('total enter amt', total_user_entered_amt)
        request.session['total_invoice_amount'] = total_user_entered_amt
        request.session['batch_no'] = batch_no
        request.session['entity_name'] = entity_name
        if total_user_entered_amt > total_invoice_amount:
            messages.error(request, "total invoice amount entered is more than the sum of the total amount of all invoices!"
                                    "you want to update total invoice amount to " + str(total_user_entered_amt) + "Rs. ?")
            return redirect('confirmation')
        elif total_user_entered_amt < total_invoice_amount:
            messages.error(request, "total invoice amount entered is less than the sum of the total amount of all invoices!"
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


def dashboard(request):
    invoices = Invoice.objects.all()
    return render(request, 'dashboard.html', {'invoices': invoices})


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
#         else:
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
    discounted_val = (face_val_discount_rate/100) * total_invoice_amount
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

        return_amt = round((((rate_of_return/100) / 365) * tenure * maturity_amount), 2)
        print(return_amt)
        investment_amt = round((maturity_amount - return_amt), 2)
        print('investment_amt', investment_amt)

        amount_due = round(((maturity_amount / investment_amt) * invested_amt), 2)
        print(amount_due)

        return_inv = amount_due - invested_amt
        print(return_inv)

        annualized_yield = round((((return_inv / invested_amt) / tenure) * 365 * 100), 2)
        print(annualized_yield)

        amt_payable_to_business = round(amount_due - (((rate_of_interest/100) / 365) * tenure * amount_due), 2)
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
                                       amount_settled_with_business=amt_payable_to_business, business_id=invoice.business_id,
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


def check(request):
    if request.method == "POST":
        invested_amt = request.GET.get['invested_amt']
        print(invested_amt)
    return render(request, 'investor/investor_deals.html')


# We can delete this:
def invoice_detail(request):
    return render(request, 'business/invoice_detail.html')


# Investor Section #

def investor_deals(request):
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    invoices = Invoice.objects.all()
    invoices = invoices[::-1]
    print(invoices)
    investor_limit = Investor.objects.get(investor_name=request.user).minimum_investment_limit
    # print(investor_limit)
    # print(invoices)
    page = request.GET.get('page', 1)

    paginator = Paginator(invoices, 2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    for i in invoices:
        entity_name = i.entity_name
        entity_object = Entity.objects.get(entity_name=entity_name)
        entity_id_ = entity_object.entity_id
        investor_id = Investor.objects.get(investor_name=request.user).id
        # print(investor_id, entity_id1)
        ror_object = EntityInvestorRORMapping.objects.get(entity_id=entity_id_, investor_id=investor_id)
        ror = ror_object.applicable_ror
        tenure = (i.invoice_due_date - date.today()).days
        return_amt = round((((ror / 100) / 365) * tenure * i.invoice_fundable_amount), 2)
        investment_amt = round((i.invoice_fundable_amount - return_amt), 2)
        total_invest = i.invoice_total_investment
        discounted_val = (i.applicable_discount_rate / 100) * i.invoice_amount
        maturity_amount = i.invoice_amount - discounted_val
        i.invoice_investment_amount = investment_amt
        i.invoice_available_investment = i.invoice_investment_amount - i.invoice_total_investment
        i.ror_for_investor = ror
        i.maturity_after_investment = maturity_amount - i.amount_due_investor
        i.save()
    if request.is_ajax() and request.method == "POST":
        invested_amt1 = float(request.POST['invested_amt'])
    #     investment_amt1 = float(request.POST['investment_amt'])
    #     ror1 = float(request.POST['ror'])
    #     maturity_amount1 = float(request.POST['maturity_amount'])
        invoice_id = request.POST['invoice_id']
        invoice_obj = Invoice.objects.get(id=invoice_id)
        due_date1 = Invoice.objects.get(id=invoice_id).invoice_due_date
        tenor = (due_date1-date.today()).days
        entity_name = invoice_obj.entity_name
        business_id = invoice_obj.business_id
        entity_obj = Entity.objects.get(entity_name=entity_name)
        entity_id2 = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
        # print(roi_obj)
        available_investment = round((invoice_obj.invoice_investment_amount - invoice_obj.invoice_total_investment), 2)
        total_investment = invoice_obj.invoice_total_investment + invested_amt1

        # if invested_amt1 < investor_limit:
        return_amount1 = round(
            (((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
        investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

        amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * invested_amt1), 2)
        print(amount_due1, i.maturity_after_investment)
        return_inv = round((amount_due1 - invested_amt1), 2)

        annualized_yield = round((((return_inv / invested_amt1) / tenor) * 365 * 100), 2)

        amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
        # print(amt_payable_to_business)

        percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
        total_subs = invoice_obj.invoice_subscription_status + percentage_subs

        after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
        print(after_investment_maturity)
        if available_investment > investor_limit:
            # print(investor_limit, invested_amt1)
            if invested_amt1 >= investor_limit:
                if invested_amt1 <= available_investment:
                    Transaction.objects.create(invoice_id=invoice_obj.id, transaction_date=date.today(),
                                               invoice_upload_date=invoice_obj.invoice_upload_date, amount_invested=invested_amt1,
                                               tenor=tenor,
                                               due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                               applicable_yield_investor=invoice_obj.ror_for_investor,
                                               settlement_amount_with_investor=amount_due1, settlement_amount_with_business=amt_payable_to_business,
                                               entity_id=entity_id2, business_id=business_id, investor_id=investor_id, batch_no=invoice_obj.batch_no,
                                               entity_name=entity_name)
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
            if invested_amt1 == available_investment:
                Transaction.objects.create(invoice_id=invoice_obj.id, transaction_date=date.today(),
                                           invoice_upload_date=invoice_obj.invoice_upload_date,
                                           amount_invested=invested_amt1,
                                           tenor=tenor,
                                           due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                           applicable_yield_investor=invoice_obj.ror_for_investor,
                                           settlement_amount_with_investor=amount_due1,
                                           settlement_amount_with_business=amt_payable_to_business,
                                           entity_id=entity_id2, business_id=business_id, investor_id=investor_id,
                                           entity_name=entity_name)
                invoice_obj.invoice_total_investment = total_investment
                invoice_obj.invoice_subscription_status = total_subs
                invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
                invoice_obj.save()
                message = 'thank you for investing1.'
            return JsonResponse({'msg': message})
            print(available_investment, invested_amt1)
            message = 'investment amount should be equal to the available amount.'
            return JsonResponse({'msg': message})
    return render(request, 'Investors/investor_deals.html', {'data': invoices, 'today': today, 'today1': today1,
                                                             'tomorrow': tomorrow, 'day_after': day_after_tom, 'yield': ror,
                                                             'investment_amt': investment_amt, 'min_amount': investor_limit,
                                                             'users': users})


def table_view(request):
    inv_id = Investor.objects.get(investor_name=request.user).id
    print(inv_id)
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    print(ror_obj)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(investor_name=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by()
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices)
    entity_ls.sort()
    print(entity_ls, invoice_ls)
    # print(invoice_ls)
    if request.method == 'POST' and request.is_ajax():
        invested_amount = float(request.POST['amt'])
        print(invested_amount)
        invoice_id = request.POST['invoice_id']
        investor_id = Investor.objects.get(investor_name=request.user).id
        print(invoice_id)
        invoice_obj = Invoice.objects.get(invoice_id=invoice_id)
        print(invoice_obj)
        due_date1 = invoice_obj.invoice_due_date
        tenor = (due_date1 - date.today()).days
        entity_name = invoice_obj.entity_name
        business_id = invoice_obj.business_id
        entity_obj = Entity.objects.get(entity_name=entity_name)
        entity_id2 = entity_obj.entity_id
        roi_obj = EntityBusinessROIMapping.objects.get(business_id=business_id, entity_id=entity_id2)
        # print(roi_obj)
        available_investment = round((invoice_obj.invoice_investment_amount - invoice_obj.invoice_total_investment), 2)
        total_investment = invoice_obj.invoice_total_investment + invested_amount

        # if invested_amt1 < investor_limit:
        return_amount1 = round(
            (((invoice_obj.ror_for_investor / 100) / 365) * tenor * invoice_obj.invoice_fundable_amount), 2)
        investment_amt1 = invoice_obj.invoice_fundable_amount - return_amount1

        amount_due1 = round(((invoice_obj.invoice_fundable_amount / investment_amt1) * invested_amount), 2)
        # print(amount_due1, i.maturity_after_investment)
        return_inv = round((amount_due1 - invested_amount), 2)

        annualized_yield = round((((return_inv / invested_amount) / tenor) * 365 * 100), 2)

        amt_payable_to_business = round(amount_due1 - ((amount_due1 * (roi_obj.applicable_roi / 100) / 365) * tenor), 2)
        # print(amt_payable_to_business)

        percentage_subs = round(((amount_due1 / invoice_obj.invoice_fundable_amount) * 100), 2)
        total_subs = invoice_obj.invoice_subscription_status + percentage_subs

        after_investment_maturity = round((invoice_obj.maturity_after_investment - amount_due1), 2)
        print(after_investment_maturity)
        if available_investment > investor_limit:
            # print(investor_limit, invested_amt1)
            if invested_amount >= investor_limit:
                if invested_amount <= available_investment:
                    Transaction.objects.create(invoice_id=invoice_obj.id, transaction_date=date.today(),
                                               invoice_upload_date=invoice_obj.invoice_upload_date,
                                               amount_invested=invested_amount,
                                               tenor=tenor,
                                               due_date=invoice_obj.invoice_due_date,
                                               applicable_ROI=roi_obj.applicable_roi,
                                               applicable_yield_investor=invoice_obj.ror_for_investor,
                                               settlement_amount_with_investor=amount_due1,
                                               settlement_amount_with_business=amt_payable_to_business,
                                               entity_id=entity_id2, business_id=business_id, investor_id=investor_id)
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
            if invested_amount == available_investment:
                Transaction.objects.create(invoice_id=invoice_obj.id, transaction_date=date.today(),
                                           invoice_upload_date=invoice_obj.invoice_upload_date,
                                           amount_invested=invested_amount,
                                           tenor=tenor,
                                           due_date=invoice_obj.invoice_due_date, applicable_ROI=roi_obj.applicable_roi,
                                           applicable_yield_investor=invoice_obj.ror_for_investor,
                                           settlement_amount_with_investor=amount_due1,
                                           settlement_amount_with_business=amt_payable_to_business,
                                           entity_id=entity_id2, business_id=business_id, investor_id=investor_id)
                invoice_obj.invoice_total_investment = total_investment
                invoice_obj.invoice_subscription_status = total_subs
                invoice_obj.maturity_after_investment = round(invoice_obj.invoice_fundable_amount - amount_due1)
                invoice_obj.save()
                message = 'thank you for investing1.'
            return JsonResponse({'msg': message})
            # print(available_investment, invested_amt1)
            message = 'investment amount should be equal to the available amount.'
            return JsonResponse({'msg': message})
    return render(request, 'investors/table_view.html', {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow, 'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_maturity(request):
    inv_id = request.user.id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(investor_name=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('invoice_due_date')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices)
    entity_ls.sort()
    print(invoice_ls)
    return render(request, 'Investors/sort/sort_maturity.html', {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow, 'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_funded(request):
    inv_id = request.user.id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(investor_name=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('invoice_subscription_status')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices)
    entity_ls.sort()
    invoice_ls = invoice_ls[::-1]
    return render(request, 'Investors/sort/sort_funded.html', {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow, 'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_available_investment(request):
    inv_id = request.user.id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(investor_name=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('invoice_available_investment')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices)
    entity_ls.sort()
    # invoice_ls = invoice_ls[::-1]
    return render(request, 'Investors/sort/sort_available_investment.html', {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow, 'min_limit': investor_limit, 'day_after': day_after_tom})


def sort_yield(request):
    inv_id = request.user.id
    ror_obj = EntityInvestorRORMapping.objects.filter(investor_id=inv_id)
    entity_ls = []
    today1 = date.today
    today = datetime.today().strftime("%d/%m/%Y")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    day_after_tom = (datetime.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    investor_limit = Investor.objects.get(investor_name=request.user).minimum_investment_limit
    for i in ror_obj:
        entity_name = Entity.objects.get(entity_id=i.entity_id).entity_name
        entity_ls.append(entity_name)
    invoice_ls = []
    for i in entity_ls:
        invoices = Invoice.objects.filter(entity_name=i).order_by('ror_for_investor')
        if len(invoices) > 1:
            for j in invoices:
                invoice_ls.append(j)
        else:
            invoice_ls.append(invoices)
    entity_ls.sort()
    # invoice_ls = invoice_ls[::-1]
    return render(request, 'Investors/sort/sort_yield.html', {'entity': entity_ls, 'users': invoice_ls, 'today': today, 'tomorrow': tomorrow, 'min_limit': investor_limit, 'day_after': day_after_tom})


def deal_details(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'Investors/deal_details.html', {'invoice': invoice})


def manage_funds(request):
    investor = request.user
    investor_id = Investor.objects.get(investor_name=investor).id
    # print(investor_id)
    transaction_list = Transaction.objects.filter(investor_id=investor_id).order_by('-transaction_date')
    print(transaction_list)
    return render(request, 'Investors/managefunds.html', {'transactions': transaction_list})


def order(request):
    investor = request.user
    investor_id = Investor.objects.get(investor_name=investor).id
    # print(investor_id)
    transaction_list = Transaction.objects.filter(investor_id=investor_id).order_by('-transaction_date')
    return render(request, 'Investors/order.html', {'transactions': transaction_list})


def add_funds(request):
    return render(request, 'Investors/addfunds.html')


def withdrawal(request):
    return render(request, 'Investors/withdrawal.html')


def help_(request):
    return render(request, 'Investors/help.html')


def transactions(request):
    transaction_list = Transaction.objects.all()
    return render(request, 'test/transactions.html', {'transaction': transaction_list})


def view_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return_inv = round((transaction.settlement_amount_with_investor - transaction.amount_invested), 2)
    return render(request, 'test/view_transaction.html', {'transaction': transaction, 'return': return_inv})


# Temp inv login , can be delete later:
def investor_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['pwd']
        user = authenticate(username=name, password=password)
        if user is not None:
            department = UserType.objects.get(user=user).department
            if department == 'investor':
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
        if user is not None:
            if user.type == 'business':
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Only for investor.')
                return redirect('business_login')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('business_login')
    return render(request, 'business/business_login.html')
