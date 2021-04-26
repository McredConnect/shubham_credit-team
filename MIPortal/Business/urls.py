from django.urls import path, include
from . import views

urlpatterns = [
    path('bank-account/', views.bank_account, name='bank-account'),
    path('bank-account-withdraw/', views.bank_account_withdraw, name='bank-account-withdraw'),
    path('create-entity/', views.create_entity, name='create-entity'),
    path('create-entity-business/', views.create_entity_business, name='create-entity-business'),
    path('create-entity-investor/', views.create_entity_investor, name='create-entity-investor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-business/', views.edit_business, name='edit-business'),
    path('help-and-support/', views.help_and_support, name='help-and-support'),
    path('invoice/', views.invoice, name='invoice'),
    path('invoice-upload/', views.invoice_upload, name='invoice-upload'),
    path('refer-and-earn/', views.refer_and_earn, name='refer-and-earn'),
    path('transactions/', views.transactions, name='transactions'),
    path('transaction-details/<uuid:pk>', views.transaction_details, name='transaction-details'),
    path('view-details/<int:mode>', views.view_details, name='view-details'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),

]