from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('deals/', views.investor_deals, name='investor_deals'),
    # path('help/', views.help_, name='help'),
    path('', views.invoice_form, name='invoice_form'),
    path('home', views.home, name='home'),
    # path('inv-dashboard', views.dashboard, name='inv-dashboard'),
    path('dashboard', views.dashboard, name='inv-dashboard'),
    # path('view-details', views.view_details, name='view-details'),
    path('inv-view-details/<int:mode>', views.view_details, name='inv-view-details'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('investor_deals', views.investor_deals, name='investor_deals'),
    path('invoice_detail', views.invoice_detail, name='invoice_detail'),
    # path('view_invoice/<int:pk>', views.view_invoice, name='view_invoice'),
    path('viewInvoice/<int:pk>', views.viewInvoice, name='viewInvoice'),
    path('view_transaction/<int:pk>', views.view_transaction, name='view_transaction'),
    path('transactions', views.transactions, name='transactions'),
    path('check', views.check, name='check'),
    path('investor_login', views.investor_login, name='investor_login'),
    path('business_login', views.business_login, name='business_login'),
    path('table_view', views.table_view, name='table_view'),
    path('table_view/sort_maturity', views.sort_maturity, name='sort_maturity'),
    path('table_view/sort_funded', views.sort_funded, name='sort_funded'),
    path('table_view/sort_available_investment', views.sort_available_investment, name='sort_available_investment'),
    path('table_view/sort_yield', views.sort_yield, name='sort_yield'),
    path('deal_details/<uuid:pk>', views.deal_details, name='deal_details'),
    path('manage_funds', views.manage_funds, name='manage_funds'),
    path('order/<int:mode>/<int:sort_order>', views.order, name='order'),
    path('inv-refer-and-earn/', views.refer_and_earn, name='inv-refer-and-earn'),
    path('add_funds', views.add_funds, name='add_funds'),
    path('change-account', views.change_account, name='change-account'),
    path('withdraw', views.withdrawal, name='withdraw'),
    path('help/', views.help, name='help'),
    path('repayment/', views.repayment, name='repayment'),
    path('update-invoice/', views.update_invoice, name='update-invoice'),
    # path('deal_details', views.deal_details, name='deal_details'),
]

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)