
from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.
from Investors.models import *
from tests.models import *

# Create your views here.
def reason(request):
    return render(request,'new_dashboard/reason.html')
def registration(request):
    return render(request, 'new_dashboard/registration.html')

def individul(request):
    form = "individual"
    print('in individual')
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    print('individual', investor_id)
    investor_obj = Investor.objects.get(investor_id=investor_id)
    name = investor_obj.investor_name
    mobile = investor_obj.contact_no
    email = investor_obj.investor_email
    dob = investor_obj.investor_date_of_incorporation
    print(dob)
    pan_num = investor_obj.investor_PAN
    pan_photo = investor_obj.investor_PAN_proof
    aadhaar_num = investor_obj.investor_Aadhaar
    aadhaar_photo = investor_obj.investor_Aadhaar_proof
    gst_num = investor_obj.investor_gs_number
    gstn_proof = investor_obj.investor_gst_proof
    gst_details = investor_obj.investor_gst_detail
    status = investor_obj.investor_login_status
    flag = 'false'
    print(status)
    if request.method == 'POST':
        flag = 'true'
        category = request.POST['category']
        status = request.POST['login_status']
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        dob = request.POST['dob']
        pan_num = request.POST['pan_num']
        pan_photo = request.FILES.get('pan_card')
        aadhaar_num = request.POST['aadhaar_num']
        aadhaar_photo = request.FILES.get('aadhaar_card')
        gst_details = request.POST['flexRadioDefault']
        gst_num = request.POST['gst_num']
        gstn_proof = request.FILES.get('gstn_proof')
        investor_obj.investor_category = category
        investor_obj.investor_login_status = status
        investor_obj.investor_name = name
        investor_obj.contact_no = mobile
        investor_obj.investor_email = email
        investor_obj.investor_date_of_incorporation = dob
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_Aadhaar = aadhaar_num
        investor_obj.investor_Aadhaar_proof = aadhaar_photo
        investor_obj.investor_gst_detail = gst_details
        if gst_details == "Yes":
            investor_obj.investor_gs_number = gst_num
            investor_obj.investor_gst_proof = gstn_proof
            investor_obj.save()
        else:
            investor_obj.investor_gs_number = ""
            investor_obj.investor_gst_proof = " "
            investor_obj.save()

        investor_obj.save()




        # obj = Investor.objects.create(investor_category=category, investor_name=name,
        #                               contact_no=mobile, investor_email=email, investor_date_of_incorporation=dob, investor_PAN=pan_num,
        #                               investor_PAN_proof=pan_photo, investor_Aadhaar=aadhaar_num, investor_Aadhaar_proof=aadhaar_photo,
        #                               investor_gst_detail=gst_details, investor_gs_number=gst_num, investor_gst_proof=gstn_proof)
        # obj.save()

        # return redirect('individual')

    context = {'investor_name':name,  'contact_no':mobile, 'investor_email':email, 'dob':dob, 'pan_num':pan_num, 'pan_photo':pan_photo,
                   'aadhaar_num': aadhaar_num, 'aadhaar_photo':aadhaar_photo,'gst_details':gst_details, 'gst_num':gst_num,
               'gstn_proof':gstn_proof,'form':form, 'status': status, 'flag':flag}



    return render(request, 'new_dashboard/individual.html', context)

def huf(request):
    form = 'huf'
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    investor_obj = Investor.objects.get(investor_id=investor_id)
    name = investor_obj.investor_name
    dof = investor_obj.investor_date_of_incorporation
    pan_num = investor_obj.investor_PAN
    pan_photo = investor_obj.investor_PAN_proof
    gst_details = investor_obj.investor_gst_detail
    auth_user = investor_obj.investor_authorised_user_name
    auth_user_mobile = investor_obj.investor_authorised_user_mobile
    auth_user_email = investor_obj.investor_authorised_user_email
    auth_user_dob = investor_obj.investor_authorised_user_DOB
    auth_user_pan = investor_obj.investor_authorised_user_PAN
    auth_user_pancard = investor_obj.investor_authorised_user_PAN_proof
    auth_user_aadhaar = investor_obj.investor_authorised_user_Aadhaar
    auth_user_aadhaarcard = investor_obj.investor_authorised_user_Aadhaar_proof
    status = investor_obj.investor_login_status
    flag = "false"
    if request.method == 'POST':
        flag = "true"
        category = request.POST['category']
        status = request.POST['login_status']
        name = request.POST['name']
        dof = request.POST['dof']
        pan_num = request.POST['pan']
        pan_photo = request.FILES.get('pan_card')
        gst_details = request.POST['gst_details']
        auth_user = request.POST['username']
        auth_user_mobile = request.POST['user_mobile']
        auth_user_email = request.POST['user_email']
        auth_user_dob = request.POST['user_dob']
        auth_user_pan = request.POST['user_pan']
        auth_user_pancard = request.FILES.get('user_pan_card')
        auth_user_aadhaar = request.POST['user_aadhaar']
        auth_user_aadhaarcard = request.FILES.get('user_aadhaar_card')
        investor_obj.investor_category = category
        investor_obj.investor_login_status = status
        investor_obj.investor_name = name
        investor_obj.investor_date_of_incorporation = dof
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_gst_detail = gst_details
        investor_obj.investor_authorised_user_name = auth_user
        investor_obj.investor_authorised_user_mobile = auth_user_mobile
        investor_obj.investor_authorised_user_DOB = auth_user_dob
        investor_obj.investor_authorised_user_email = auth_user_email
        investor_obj.investor_authorised_user_PAN = auth_user_pan
        investor_obj.investor_authorised_user_PAN_proof = auth_user_pancard
        investor_obj.investor_authorised_user_Aadhaar = auth_user_aadhaar
        investor_obj.investor_authorised_user_Aadhaar_proof = auth_user_aadhaarcard
        investor_obj.save()

    context = {'name': name, 'dof': dof, 'pan': pan_num, 'pancard': pan_photo, 'gst_details': gst_details,
               'auth_user': auth_user, 'auth_user_mobile': auth_user_mobile, 'auth_user_email': auth_user_email, 'auth_user_dob': auth_user_dob, 'auth_user_pan': auth_user_pan,
               'auth_user_pancard': auth_user_pancard,'auth_user_aadhaar': auth_user_aadhaar, 'auth_user_aadhaarcard': auth_user_aadhaarcard,'flag':flag, 'form': form, 'status': status}
        # return redirect('huf')

    return render(request, 'new_dashboard/huf.html',context)

def partnership_llp(request):
    form = "partnership_llp"
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    investor_obj = Investor.objects.get(investor_id=investor_id)
    name = investor_obj.investor_name
    dof = investor_obj.investor_date_of_incorporation
    pan_num = investor_obj.investor_PAN
    pan_photo = investor_obj.investor_PAN_proof
    coi = investor_obj.investor_cert_incorporation
    resolution_cert = investor_obj.investor_resolution
    gst_details = investor_obj.investor_gst_detail
    auth_user = investor_obj.investor_authorised_user_name
    auth_user_mobile = investor_obj.investor_authorised_user_mobile
    auth_user_email = investor_obj.investor_authorised_user_email
    auth_user_dob = investor_obj.investor_authorised_user_DOB
    auth_user_pan = investor_obj.investor_authorised_user_PAN
    auth_user_pancard = investor_obj.investor_authorised_user_PAN_proof
    auth_user_aadhaar = investor_obj.investor_authorised_user_Aadhaar
    auth_user_aadhaarcard = investor_obj.investor_authorised_user_Aadhaar_proof
    status = investor_obj.investor_login_status
    flag = "false"
    if request.method == 'POST':
        flag = "true"
        category = request.POST['category']
        status = request.POST['login_status']
        name = request.POST['name']
        dof = request.POST['dof']
        pan_num = request.POST['pan']
        pan_photo = request.FILES.get('pan_card')
        coi = request.FILES.get('coi')
        resolution_cert = request.FILES.get('resolution')
        gst_details = request.POST['gst_details']
        auth_user = request.POST['username']
        auth_user_mobile = request.POST['user_mobile']
        auth_user_email = request.POST['user_email']
        auth_user_dob = request.POST['user_dob']
        auth_user_pan = request.POST['user_pan']
        auth_user_pancard = request.FILES.get('user_pan_card')
        auth_user_aadhaar = request.POST['user_aadhaar']
        auth_user_aadhaarcard = request.FILES.get('user_aadhaar_card')
        investor_obj.investor_category = category
        investor_obj.investor_login_status = status
        investor_obj.investor_name = name
        investor_obj.investor_date_of_incorporation = dof
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_gst_detail = gst_details
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_cert_incorporation = coi
        investor_obj.investor_resolution = resolution_cert
        investor_obj.investor_authorised_user_name = auth_user
        investor_obj.investor_authorised_user_mobile = auth_user_mobile
        investor_obj.investor_authorised_user_DOB = auth_user_dob
        investor_obj.investor_authorised_user_email = auth_user_email
        investor_obj.investor_authorised_user_PAN = auth_user_pan
        investor_obj.investor_authorised_user_PAN_proof = auth_user_pancard
        investor_obj.investor_authorised_user_Aadhaar = auth_user_aadhaar
        investor_obj.investor_authorised_user_Aadhaar_proof = auth_user_aadhaarcard
        investor_obj.save()


        # return redirect('partnership_llp')
    context = {'name': name, 'dof': dof, 'pan': pan_num, 'pancard': pan_photo, 'coi': coi, 'resolution': resolution_cert, 'gst_details': gst_details,
               'auth_user': auth_user, 'auth_user_mobile': auth_user_mobile, 'auth_user_email': auth_user_email, 'auth_user_dob': auth_user_dob, 'auth_user_pan': auth_user_pan,
               'auth_user_pancard': auth_user_pancard, 'auth_user_aadhaar': auth_user_aadhaar, 'auth_user_aadhaarcard': auth_user_aadhaarcard, 'flag':flag, 'form': form, 'status': status}

    return render(request, 'new_dashboard/partnership_llp.html',context)

def private_ltd(request):
    form = 'private_ltd'
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    investor_obj = Investor.objects.get(investor_id=investor_id)
    name = investor_obj.investor_name
    dof = investor_obj.investor_date_of_incorporation
    pan_num = investor_obj.investor_PAN
    pan_photo = investor_obj.investor_PAN_proof
    coi = investor_obj.investor_cert_incorporation
    resolution_cert = investor_obj.investor_resolution
    gst_details = investor_obj.investor_gst_detail
    auth_user = investor_obj.investor_authorised_user_name
    auth_user_mobile = investor_obj.investor_authorised_user_mobile
    auth_user_email = investor_obj.investor_authorised_user_email
    auth_user_dob = investor_obj.investor_authorised_user_DOB
    auth_user_pan = investor_obj.investor_authorised_user_PAN
    auth_user_pancard = investor_obj.investor_authorised_user_PAN_proof
    auth_user_aadhaar = investor_obj.investor_authorised_user_Aadhaar
    auth_user_aadhaarcard = investor_obj.investor_authorised_user_Aadhaar_proof
    status = investor_obj.investor_login_status
    flag = "false"

    if request.method == 'POST':
        flag = "true"
        category = request.POST['category']
        status = request.POST['login_status']
        name = request.POST['name']
        dof = request.POST['dof']
        pan_num = request.POST['pan']
        pan_photo = request.FILES.get('pan_card')
        coi = request.FILES.get('coi')
        resolution_cert = request.FILES.get('resolution')
        gst_details = request.POST['gst_details']
        auth_user = request.POST['username']
        auth_user_mobile = request.POST['user_mobile']
        auth_user_email = request.POST['user_email']
        auth_user_dob = request.POST['user_dob']
        auth_user_pan = request.POST['user_pan']
        auth_user_pancard = request.FILES.get('user_pan_card')
        auth_user_aadhaar = request.POST['user_aadhaar']
        auth_user_aadhaarcard = request.FILES.get('user_aadhaar_card')
        investor_obj.investor_category = category
        investor_obj.investor_login_status = status
        investor_obj.investor_name = name
        investor_obj.investor_date_of_incorporation = dof
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_gst_detail = gst_details
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_cert_incorporation = coi
        investor_obj.investor_resolution = resolution_cert
        investor_obj.investor_authorised_user_name = auth_user
        investor_obj.investor_authorised_user_mobile = auth_user_mobile
        investor_obj.investor_authorised_user_DOB = auth_user_dob
        investor_obj.investor_authorised_user_email = auth_user_email
        investor_obj.investor_authorised_user_PAN = auth_user_pan
        investor_obj.investor_authorised_user_PAN_proof = auth_user_pancard
        investor_obj.investor_authorised_user_Aadhaar = auth_user_aadhaar
        investor_obj.investor_authorised_user_Aadhaar_proof = auth_user_aadhaarcard
        investor_obj.save()
        status = True

    context = {'name': name, 'dof': dof, 'pan': pan_num, 'pancard': pan_photo, 'coi': coi, 'resolution': resolution_cert, 'gst_details': gst_details,
               'auth_user': auth_user, 'auth_user_mobile': auth_user_mobile, 'auth_user_email': auth_user_email, 'auth_user_dob': auth_user_dob, 'auth_user_pan': auth_user_pan,
                   'auth_user_pancard': auth_user_pancard, 'status': status, 'auth_user_aadhaar': auth_user_aadhaar, 'auth_user_aadhaarcard': auth_user_aadhaarcard, 'flag':flag,'form': form}
        # return redirect('private_ltd')
    return render(request, 'new_dashboard/private_ltd.html', context)

def nbfc_bank(request):
    form = "nbfc_bank"
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    investor_obj = Investor.objects.get(investor_id=investor_id)
    name = investor_obj.investor_name
    dof = investor_obj.investor_date_of_incorporation
    pan_num = investor_obj.investor_PAN
    pan_photo = investor_obj.investor_PAN_proof
    coi = investor_obj.investor_cert_incorporation
    resolution_cert = investor_obj.investor_resolution
    gst_details = investor_obj.investor_gst_detail
    auth_user = investor_obj.investor_authorised_user_name
    auth_user_mobile = investor_obj.investor_authorised_user_mobile
    auth_user_email = investor_obj.investor_authorised_user_email
    auth_user_dob = investor_obj.investor_authorised_user_DOB
    auth_user_pan = investor_obj.investor_authorised_user_PAN
    auth_user_pancard = investor_obj.investor_authorised_user_PAN_proof
    auth_user_aadhaar = investor_obj.investor_authorised_user_Aadhaar
    auth_user_aadhaarcard = investor_obj.investor_authorised_user_Aadhaar_proof
    status = investor_obj.investor_login_status
    print("status", status)
    flag = "false"

    if request.method == 'POST':
        flag = "true"
        category = request.POST['category']
        status = request.POST['login_status']
        print(status)
        name = request.POST['name']
        dof = request.POST['dof']
        pan_num = request.POST['pan']
        pan_photo = request.FILES.get('pan_card')
        coi = request.FILES.get('coi')
        resolution_cert = request.FILES.get('resolution')
        gst_details = request.POST['gst_details']
        auth_user = request.POST['username']
        auth_user_mobile = request.POST['user_mobile']
        auth_user_email = request.POST['user_email']
        auth_user_dob = request.POST['user_dob']
        auth_user_pan = request.POST['user_pan']
        auth_user_pancard = request.FILES.get('user_pan_card')
        auth_user_aadhaar = request.POST['user_aadhaar']
        auth_user_aadhaarcard = request.FILES.get('user_aadhaar_card')
        investor_obj.investor_category = category
        investor_obj.investor_login_status = status
        investor_obj.investor_name = name
        investor_obj.investor_date_of_incorporation = dof
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_gst_detail = gst_details
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_cert_incorporation = coi
        investor_obj.investor_resolution = resolution_cert
        investor_obj.investor_authorised_user_name = auth_user
        investor_obj.investor_authorised_user_mobile = auth_user_mobile
        investor_obj.investor_authorised_user_DOB = auth_user_dob
        investor_obj.investor_authorised_user_email = auth_user_email
        investor_obj.investor_authorised_user_PAN = auth_user_pan
        investor_obj.investor_authorised_user_PAN_proof = auth_user_pancard
        investor_obj.investor_authorised_user_Aadhaar = auth_user_aadhaar
        investor_obj.investor_authorised_user_Aadhaar_proof = auth_user_aadhaarcard
        investor_obj.save()


        # return redirect('nbfc_bank')
    context = {'name': name, 'dof': dof, 'pan': pan_num, 'pancard': pan_photo, 'coi': coi, 'resolution': resolution_cert, 'gst_details': gst_details,
                   'auth_user': auth_user, 'auth_user_mobile': auth_user_mobile, 'auth_user_email': auth_user_email, 'auth_user_dob': auth_user_dob, 'auth_user_pan': auth_user_pan,
                   'auth_user_pancard': auth_user_pancard, 'status': status, 'auth_user_aadhaar': auth_user_aadhaar, 'auth_user_aadhaarcard': auth_user_aadhaarcard, 'form': form, 'flag':flag}
    return render(request, 'new_dashboard/nbfc_bank.html',context)


def NRI(request):
    form = "NRI"
    investor_id = Investor.objects.get(user_id=request.user).investor_id
    investor_obj = Investor.objects.get(investor_id=investor_id)
    name = investor_obj.investor_name
    email = investor_obj.investor_email
    mobile = investor_obj.contact_no
    dob = investor_obj.investor_date_of_incorporation
    pan_num = investor_obj.investor_PAN
    pan_photo = investor_obj.investor_PAN_proof
    nri_proof = investor_obj.investor_NRI_proof
    gst_details = investor_obj.investor_gst_detail
    print(gst_details)
    gst_num = investor_obj.investor_gs_number
    gstn_proof = investor_obj.investor_gst_proof
    status = investor_obj.investor_login_status
    print(status)
    flag = "false"


    if request.method == 'POST':
        flag = "true"
        category = request.POST['category']
        status = request.POST['login_status']
        print(status)
        name = request.POST['name']
        dob = request.POST['dob']
        mobile = request.POST['mobile']
        email = request.POST['email']
        pan_num = request.POST['pan']
        pan_photo = request.FILES.get('pan_card')
        nri_proof = request.FILES.get('nri_proof')
        gst_details = request.POST['gst_details']
        gst_num = request.POST['gst_num']
        gstn_proof = request.FILES.get('gstn_proof')
        investor_obj.investor_category = category
        investor_obj.investor_login_status = status
        investor_obj.investor_name = name
        investor_obj.contact_no = mobile
        investor_obj.investor_email = email
        investor_obj.investor_date_of_incorporation = dob
        investor_obj.investor_PAN = pan_num
        investor_obj.investor_PAN_proof = pan_photo
        investor_obj.investor_NRI_proof = nri_proof
        investor_obj.investor_gst_detail = gst_details
        investor_obj.investor_gs_number = gst_num
        investor_obj.investor_gst_proof = gstn_proof
        investor_obj.save()


        # return redirect('NRI')
    context = {'name': name, 'email': email, 'mobile': mobile, 'dob': dob, 'pan': pan_num, 'pan_card': pan_photo,
                   'nri_proof': nri_proof, 'gst_details': gst_details,
                   'gst_num': gst_num, 'gstn_proof': gstn_proof, 'form': form, 'status': status, 'flag':flag}

    return render(request, 'new_dashboard/NRI.html', context)

def transaction(request):
    return render(request, 'new_dashboard/transaction.html')


def settlement(request):
    return render(request, 'new_dashboard/settlement.html')

# def logout(request):
#     del request.session['logged_in']
#     return redirect('mcred_login')
def user_logout(request):
    logout(request)
    return redirect('mcred_login')