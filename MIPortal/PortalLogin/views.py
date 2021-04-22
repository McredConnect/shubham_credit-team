from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from .models import Lead
from django.core.mail import send_mail
from Investors.models import *
from accounts.models import *
from PortalLogin.models import *
from InvestorDashboards.views import *
import math, random
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.utils.timezone import datetime
import datetime
from django.shortcuts import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.template.loader import render_to_string


CustomUser = get_user_model()

# Create your views here.


def index(request):
    return render(request, 'PortalLogin/home.html')




def business(request):
    if request.method == 'POST':
        lead_type = 'business'
        name = request.POST['FullName']
        email = request.POST['Email']
        mobile_no = request.POST['mob']
        company_name = request.POST['company']
        if not mobile_no[0] in [9, 7, 8] and len(mobile_no) != 10:
            messages.error(request, 'Please enter valid mobile number')
            return redirect('mcred_business')
        else:
            # print(name, email, mobile_no, company_name)
            Lead.objects.create(type=lead_type, name=name, email=email, mobile_no=mobile_no, company_name=company_name)
            send_mail(
                'Lead Received for ' + lead_type,
                'Lead for ' + lead_type + '\n Name = ' + name + '\n Email = ' + email + '\n Mobile No. = ' + mobile_no
                + '\n Company Name = ' + company_name,
                'alerts@mcred.com',
                ['web@mcred.com'],
                fail_silently=False,
            )
    return render(request, 'PortalLogin/business.html')


def investor(request):
    if request.method == 'POST':
        lead_type = 'investor'
        name = request.POST['FullName']
        email = request.POST['Email']
        mobile_no = request.POST['mob']
        company_name = request.POST['company']
        if not mobile_no[0] in [9, 7, 8] and len(mobile_no) != 10:
            messages.error(request, 'Please enter valid mobile number')
            return redirect('mcred_investor')
        else:
            # print(name, email, mobile_no, company_name)
            Lead.objects.create(type=lead_type, name=name, email=email, mobile_no=mobile_no, company_name=company_name)
        send_mail(
            'Lead Received for ' + lead_type,
            'Lead for ' + lead_type + '\n Name = ' + name + '\n Email = ' + email + '\n Mobile No. = ' + mobile_no
            + '\n Company Name = ' + company_name,
            'alerts@mcred.com',
            ['web@mcred.com'],
            fail_silently=False,
        )
    return render(request, 'PortalLogin/investor.html')


def partner(request):
    if request.method == 'POST':
        lead_type = 'partner'
        name = request.POST['FullName']
        email = request.POST['Email']
        mobile_no = request.POST['mob']
        company_name = request.POST['company']
        if not mobile_no[0] in [9, 7, 8] and len(mobile_no) != 10:
            messages.error(request, 'Please enter valid mobile number')
            return redirect('mcred_partner')
        else:
            # print(name, email, mobile_no, company_name)
            Lead.objects.create(type=lead_type, name=name, email=email, mobile_no=mobile_no, company_name=company_name)
        send_mail(
            'Lead Received for ' + lead_type,
            'Lead for ' + lead_type + '\n Name = ' + name + '\n Email = ' + email + '\n Mobile No. = ' + mobile_no
            + '\n Company Name = ' + company_name,
            'alerts@mcred.com',
            ['web@mcred.com'],
            fail_silently=False,
        )
    return render(request, 'PortalLogin/partner.html')


def about_us(request):
    return render(request, 'PortalLogin/aboutus.html')


def blogs(request):
    objs = Blog.objects.all().order_by('-created_date')
    all_post = Paginator(objs, 4)
    page = request.GET.get('page')
    if request.method == "POST":
        num = request.POST.get('num')
        posts = all_post.page(num)
    else:
        try:
            posts = all_post.page(page)
            print('post1', posts)
        except PageNotAnInteger:
            posts=all_post.page(1)
            print('post2', posts)
        except EmptyPage:
            posts = all_post.page(all_post.num_pages)
    context = {'objs': objs, 'posts': posts}
    return render(request, 'PortalLogin/blogs.html', context)

def detailed_blog(request,pk):
    print(pk)
    blog_obj = Blog.objects.get(id=pk)
    recent_blog = Blog.objects.all().order_by('-created_date')
    category = blog_obj.category.upper()
    blog_acc_category = Blog.objects.filter(category=category)
    title = blog_obj.title
    print(title)
    context = {'blog_obj':blog_obj, 'category':category, 'recent_blog':recent_blog, 'blog_acc_category':blog_acc_category, 'title1':title}
    return render(request, 'PortalLogin/detailed_blog.html',context)


def search(request):
    # return HttpResponse('This is search')
    search = request.GET.get('search')
    posts_obj = Blog.objects.all().filter(Q(title__icontains=search))
    page = request.GET.get('page')
    paginator = Paginator(posts_obj, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts_obj': posts_obj, 'posts': posts, 'search':search}
    return render(request, 'PortalLogin/search.html', context)




def filter_data(request):
    print("In filterdata")
    categories = request.GET.getlist('_filterkey[]')
    print(categories)
    posts1 = Blog.objects.all()
    if len(categories) > 0:
        filter_post = posts1.filter(category__in=categories).order_by('-created_date')
    # print(filter_post)
    # print(filter_post.count())

    # all_post = Paginator(filter_post, 2)
    # page = request.GET.get('page')
    # print(page)
    # if request.method == "POST":
    #     num = request.POST.get('num')
    #     posts_pagination = all_post.page(num)
    # else:
    # try:
    #     posts_pagination = all_post.page(page)
    #     print('post1', posts_pagination)
    # except PageNotAnInteger:
    #     posts_pagination = all_post.page(1)
    #     print('post2', posts_pagination), 'posts_pagination':posts_pagination
    # except EmptyPage:
    #     posts_pagination = all_post.page(all_post.num_pages)
    t = render_to_string('PortalLogin/categories_list.html', {'data': filter_post})
    return JsonResponse({'data': t})

def like(request, pk):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Blog.objects.get(id=post_id)
        type = request.POST.get('detailed_page')
        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)
        if type == 'detailed_page':
            # return HttpResponseRedirect(reverse('mcred_detailed_blog', args=[str(pk)]))
            return redirect("mcred_detailed_blog", post_id)

    return redirect('mcred_blogs')



def popularity(request):
    print('in popularity')
    posts = Blog.objects.all().order_by('-likes')
    print(posts)
    t = render_to_string('PortalLogin/popularity.html', {'posts': posts})
    return JsonResponse({'data': t})

def recent(request):
    print('in recent')
    posts = Blog.objects.all().order_by('-created_date')
    print(posts)
    t = render_to_string('PortalLogin/recent.html', {'posts': posts})
    return JsonResponse({'data': t})

def demo(request):
    return render(request, 'PortalLogin/demo.html')

def bloginput(request):
    # form = blogform()
    # context = {'form': form}
    # if request.method == 'POST':
    #     form = blogform(request.POST or None, request.FILES or None)
    #     # print(form)
    #     if form.is_valid():
    #         form.save()
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES.get('image')
        description = request.POST['description']
        author = request.POST['author']
        category = request.POST['category']
        obj = Blog.objects.create(image=image, description=description, title=title, author=author, category=category)
        # if obj:
        #     return render('bloginput')

    return render(request, 'PortalLogin/demo.html')

def login(request):
    # print("login",request.session['business_id'])
    # investor_id = Investor.objects.get(user_id=request.user).investor_id
    # print(investor_id)
    # investor_obj = Investor.objects.get(investor_id=investor_id)
    # print(investor_obj)
    # type = investor_obj.investor_category
    # type = None

    # print('type',type)
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        user_type = request.POST.get('userType')
        user = authenticate(username=username, password=password)
        user1 = CustomUser.objects.get(username=username)
        print("user1",user1.id)
        print("USERTYPE",user_type)
        print("SUPERUSER",user.is_superuser)

        if user.is_superuser and user_type=="Admin":
            return redirect('business')
        try:
            inv_obj = Investor.objects.get(user_id_id=user1)
            print('inves',inv_obj.investor_category)
            print(user)
            type = inv_obj.investor_category
        except:
            inv_obj = None
            type = None
        if user_type:
            if user is not None:
                if user_type in user.type:
                    auth.login(request, user)
                    # print(auth.login(request, user))
                    print(request.user)
                    request.session['logged_in'] = True
                    if user_type == 'investor' and type == None:
                        return redirect('registration_newdashboard')
                    elif user_type == 'investor' and type == "Individual":
                        return redirect('individual')
                    elif user_type == 'investor' and type == "HUF":
                        return redirect('huf')
                    elif user_type == 'investor' and type == "Partnership / LLP":
                        return redirect('partnership_llp')
                    elif user_type == 'investor' and type == "Private Limited":
                        return redirect('private_ltd')
                    elif user_type == 'investor' and type == "NBFC / Bank":
                        return redirect('nbfc_bank')
                    elif user_type == 'investor' and type == "NRI":
                        return redirect('NRI')
                    else:
                        user_type == 'business'
                        return redirect('company_details_two')
                else:
                    messages.error(request, 'user not registered as ' + user_type + '!')
                    return redirect('mcred_login')
            else:
                messages.error(request, 'user not registered!')
                return redirect('mcred_login')
        else:
            messages.error(request, 'please select user type!')
            return redirect('mcred_login')
    return render(request, 'PortalLogin/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        corpus = '0123456789'
        size = 4
        generate_OTP = ""
        length = len(corpus)
        for i in range(size):
            generate_OTP += corpus[math.floor(random.random() * length)]
        print(generate_OTP)
        time = datetime.datetime.now()
        send_time = time.strftime("%d-%b-%Y (%H:%M:%S)")
        request.session['send_time'] = send_time

        exp_time = time + datetime.timedelta(minutes=10)
        validate_time = exp_time.strftime("%d-%b-%Y (%H:%M:%S)")
        request.session['validate_time'] = validate_time

        print(time)
        send_mail(
            'OTP Generated for ' + email,
            'OTP to change password for Mcred.com is ' + str(generate_OTP),
            'alerts@mcred.com',
            [email],
            fail_silently=False,
        )
        print(email)
        return redirect('reset_password')
    return render(request, 'PortalLogin/forgotpassword.html')


def login_otp(request):
    return render(request, 'PortalLogin/login_otp.html')


def signup(request):
    return render(request, 'PortalLogin/signup.html')


def investor_signup(request):
    if request.method == 'POST':
        user_type = 'investor'
        firstName = request.POST['FirstName']
        lastName = request.POST['LastName']
        email = request.POST['Email']
        password = request.POST['Password']
        password1 = request.POST['ConfirmPassword']
        mobile_no = request.POST['MobileNo']
        organization = request.POST['Organization']
        otp = request.POST['MobileOTP']
        referral = request.POST['ReferralCode']
        # print(firstName, lastName, email, password, password1, mobile_no, organization, otp, referral)

        msg = ''
        if password != '' and password == password1:
            count = CustomUser.objects.filter(username=email)
            if len(count) < 1:
                user = CustomUser(first_name=firstName, last_name=lastName, username=email, type=user_type,
                                  organisation=organization, mobile_no=mobile_no, referral=referral)
                user.set_password(password)
                user.save()
                print(user)
                ob = Investor.objects.create(investor_name=user.first_name + ' ' + user.last_name, user_id=user)
                print(ob.investor_id)
                request.session['investor_id']=str(ob.investor_id)
                return redirect('mcred_login')
            elif len(count) > 0 and len(count) < 2:
                user = CustomUser.objects.get(username=email)
                investor = Investor.objects.filter(user_id=user)
                if user_type in user.type:
                    if len(business) < 1:
                        Investor.objects.create(investor_name=user.first_name + ' ' + user.last_name, user_id=user)
                        return redirect('mcred_login')
                    else:
                        msg = 'user'
                        messages.error(request, 'User already registered as ' + user_type)
                else:
                    types = user.type
                    user.type = types + ',' + user_type
                    user.save()
                    Investor.objects.create(investor_name=user.first_name + ' ' + user.last_name, user_id=user)
        else:
            if password == '':
                msg = 'password'
                messages.error(request, 'Please Enter a Password!')
            else:
                msg = 'password'
                messages.error(request, 'Password Mismatched!')
        return render(request, 'PortalLogin/investor_signup.html', {'msg': msg})
    return render(request, 'PortalLogin/investor_signup.html')


def business_signup(request):
    turnover = Turnover.objects.all().order_by('number')
    states = State.objects.all().order_by('name')
    if request.method == 'POST':
        user_type = 'business'
        firstName = request.POST['FirstName']
        lastName = request.POST['LastName']
        email = request.POST['Email']
        password = request.POST['Password']
        password1 = request.POST['ConfirmPassword']
        mobile_no = request.POST['MobileNo']
        organization = request.POST['Organization']
        otp = request.POST['MobileOTP']
        turnover = request.POST['TurnoverID']
        pan = request.POST['PAN']
        city = request.POST['City']
        state = request.POST['StateID']
        # print(firstName, lastName, email, password, password1, mobile_no, organization, otp, referral)

        msg = ''
        if password != '' and password == password1:
            count = CustomUser.objects.filter(username=email)
            if len(count) < 1:
                user = CustomUser(first_name=firstName, last_name=lastName, username=email, type=user_type,
                                  organisation=organization, mobile_no=mobile_no)
                user.set_password(password)
                user.save()
                business_obj = Business.objects.create(business_name=user.first_name + ' ' + user.last_name, user_id=user, city=city,
                                        turnover=turnover, state=state, business_pan_card=pan)
                print(business_obj.business_id)
                request.session['business_id'] = str(business_obj.business_id)
                print("firstloop",request.session['business_id'])
                return redirect('mcred_login')
                # return redirect('home')
            elif len(count) > 0 and len(count) < 2:
                user = CustomUser.objects.get(username=email)
                business = Business.objects.filter(user_id=user)
                if user_type in user.type:
                    if len(business) < 1:
                        business_obj = Business.objects.create(business_name=user.first_name + ' ' + user.last_name, user_id=user,
                                                city=city,
                                                turnover=turnover, state=state, business_pan_card=pan)
                        print(business_obj.business_id)
                        request.session['business_id'] = str(business_obj.business_id)
                        print("second loop",request.session['business_id'])
                        return redirect('mcred_login')
                    else:
                        msg = 'user'
                        messages.error(request, 'User already registered as ' + user_type)
                else:
                    types = user.type
                    user.type = types + ',' + user_type
                    user.save()
                    business_obj = Business.objects.create(business_name=user.first_name + ' ' + user.last_name, user_id=user,
                                            city=city,
                                            turnover=turnover, state=state, business_pan_card=pan)
                    print(business_obj.business_id)
                    request.session['business_id'] = str(business_obj.business_id)
                    print("third loop",request.session['business_id'])


        else:
            if password == '':
                msg = 'password'
                messages.error(request, 'Please Enter a Password!')
            else:
                msg = 'password'
                messages.error(request, 'Password Mismatched!')
        return render(request, 'PortalLogin/business_signup.html', {'msg': msg})
    return render(request, 'PortalLogin/business_signup.html', {'turnover': turnover, 'states': states})


def partner_signup(request):
    states = State.objects.all().order_by('name')
    if request.method == 'POST':
        user_type = 'partner'
        firstName = request.POST['FirstName']
        lastName = request.POST['LastName']
        email = request.POST['Email']
        password = request.POST['Password']
        password1 = request.POST['ConfirmPassword']
        mobile_no = request.POST['MobileNo']
        otp = request.POST['MobileOTP']
        city = request.POST['City']
        state = request.POST['StateID']
        msg = ''
        if password != '' and password == password1:
            count = CustomUser.objects.filter(username=email)
            if len(count) < 1:
                user = CustomUser(first_name=firstName, last_name=lastName, username=email, type=user_type,
                                  mobile_no=mobile_no)
                user.set_password(password)
                user.save()
                return redirect('mcred_login')
            elif len(count) > 0 and len(count) < 2:
                user = CustomUser.objects.get(username=email)
                if user_type in user.type:
                    msg = 'user'
                    messages.error(request, 'User already registered as ' + user_type)
                else:
                    types = user.type
                    user.type = types + ',' + user_type
                    user.save()
        else:
            if password == '':
                msg = 'password'
                messages.error(request, 'Please Enter a Password!')
            else:
                msg = 'password'
                messages.error(request, 'Password Mismatched!')
        return render(request, 'PortalLogin/partner_signup.html', {'msg': msg})
    return render(request, 'PortalLogin/partner_signup.html', {'states': states})


def terms_conditions(request):
    return render(request, 'PortalLogin/terms_conditions.html')


def privacy_policy(request):
    return render(request, 'PortalLogin/privacypolicy.html')

def mcred_faqs(request):
    return render(request, 'PortalLogin/faqs.html')


def otp(request):
    url = "https://api-alerts.kaleyra.com/v4/?api_key=A8f6efc8c8a61baff223974cb3fd93ac3&method=sms&message=hello&to=9702176172&sender=HXAP1682964149IN"

    payload = {}
    files = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text.encode('utf8'))
    return render(request, 'PortalLogin/investor_signup.html')


def reset_password(request):
    time = request.session['send_time']
    validate_time = request.session['validate_time']
    if request.method == "POST":
        # otp = request.
        submit_time = datetime.datetime.now()
        submit_time = submit_time.strftime("%d-%b-%Y (%H:%M:%S)")
        if validate_time < submit_time:
            print(True)
        else:
            print(False)
        print(submit_time, validate_time)
    return render(request, 'PortalLogin/reset.html')
