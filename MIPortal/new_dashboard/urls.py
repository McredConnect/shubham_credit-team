from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registration/', views.registration, name='registration_newdashboard'),
    path('individual/', views.individul, name='individual'),
    path('huf/', views.huf, name='huf'),
    path('partnership_llp/', views.partnership_llp, name='partnership_llp'),
    path('private_ltd/', views.private_ltd, name='private_ltd'),
    path('nbfc_bank/', views.nbfc_bank, name='nbfc_bank'),
    path('NRI/', views.NRI, name='NRI'),
    path('reason/', views.reason, name='reason'),
    path('transaction/', views.transaction, name='transaction'),
    path('settlement/', views.settlement, name='settlement'),
    path('logout/', views.user_logout, name='logout'),
]