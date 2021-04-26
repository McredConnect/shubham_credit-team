from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index1"),
    path('mcred_business/', views.business, name="mcred_business"),
    path('mcred_investor/', views.investor, name="mcred_investor"),
    path('mcred_partner/', views.partner, name="mcred_partner"),
    path('mcred_aboutus/', views.about_us, name="mcred_aboutus"),
    path('mcred_blogs/', views.blogs, name="mcred_blogs"),
    path('mcred_detailed_blog<int:pk>/', views.detailed_blog, name="mcred_detailed_blog"),
    path('search/', views.search, name="search"),
    path('blog_input/', views.bloginput, name="bloginput"),
    path('filter_data/', views.filter_data, name="filter_data"),
    path('popularity/', views.popularity, name="popularity"),
    path('recent/', views.recent, name="recent"),
    path('like<int:pk>/', views.like, name="like"),
    path('mcred_login/', views.login, name="mcred_login"),
    path('mcred_forgot_password/', views.forgot_password, name="mcred_forgot_pw"),
    path('#/', views.login_otp, name="mcred_otplogin"),
    path('signup/', views.signup, name="mcred_signup"),
    path('signup/investor_signup/', views.investor_signup, name="mcred_investor_signup"),
    path('signup/business_signup/', views.business_signup, name="mcred_business_signup"),
    path('signup/partner_signup/', views.partner_signup, name="mcred_partner_signup"),
    path('terms_conditions/', views.terms_conditions, name="mcred_terms_conditions"),
    path('privacy_policy/', views.privacy_policy, name="mcred_privacy_policy"),
    path('mcred_faqs/', views.mcred_faqs, name="mcred_faqs"),
    path('otp/', views.otp, name="otp"),
    path('reset_password/', views.reset_password, name="reset_password"),
]