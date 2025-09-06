from django.urls import path
from . import views,  utils

urlpatterns = [
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),

    # Invoices
    path('invoice/add/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),

    # Export
    path('invoice/<int:pk>/pdf/', utils.export_invoice_pdf, name='export_invoice_pdf'),
]
