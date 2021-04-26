from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('bank_details', views.bank_detail, name='bank_details'),
    path('business_detail', views.business_detail, name='business_detail'),
    path('business', views.business, name='business'),
    path('business_info', views.business_info, name='business_info'),
    path('bank_statement_two', views.bank_statement_two, name='bank_statement_two'),
    path('bank_statement_details', views.bank_statement_details, name='bank_statement_details'),
    path('company_details_two', views.company_details, name='company_details_two'),
    path('gst_details', views.gst_details, name='gst_details'),
    path('index2', views.index, name='index'),

    path('gst_details_one', views.gstdetails_one, name='gst_details_one'),
    path('gst_details_2a', views.gstdetails_two_A, name='gst_details2a'),
    path('gst_details_3b', views.gstdetails_three_b, name='gst_details_3B'),
    path('pan_details', views.pan_details, name='pan_details'),
    path('financials/', views.financials, name='financials'),
    path('customers/', views.customers, name='customers'),
    path('customers2/', views.customers2, name='customers2'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers2/', views.suppliers2, name='suppliers2'),
    path('registration/', views.registration, name='registration'),
    path('home/', views.home, name='home'),
    path('as_26/', views.as_26, name='as_26'),
    path('creditrating/', views.creditrating, name='creditrating'),
    path('shareholding_two/', views.shareholding_two, name='shareholding_two'),
    # path('shareholding1/', views.shareholding1, name='shareholding1'),
    path('directors/', views.directors, name='directors'),
    path('debt/', views.debt, name='debt'),
    # path('userdetails/', views.userdetails, name='userdetails'),
    path('bank_acc_details/', views.bank_acc_details, name='bank_acc_details'),
    path('auth_userdetails/', views.auth_userdetails, name='auth_userdetails'),
    path('test1', views.test1, name='test1'),
    path('test2/<str:pk>', views.test2, name='test2'),
    path('logout/', views.user_logout, name='logout'),
]
