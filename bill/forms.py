from django import forms
from .models import Customer, Product, Invoice, InvoiceItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

