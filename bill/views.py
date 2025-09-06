from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, Invoice, InvoiceItem
from .forms import CustomerForm, ProductForm
from django.db import transaction

# Customer CRUD
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "billing/customer_list.html", {"customers": customers})

def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("customer_list")
    return render(request, "billing/customer_form.html", {"form": form})

# Product CRUD
def product_list(request):
    products = Product.objects.all()
    return render(request, "billing/product_list.html", {"products": products})

def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "billing/product_form.html", {"form": form})

# Invoice Creation
@transaction.atomic
def invoice_create(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        customer = get_object_or_404(Customer, id=customer_id)
        invoice = Invoice.objects.create(invoice_no="INV001", customer=customer)

        total, tax_total = 0, 0
        for i in range(len(request.POST.getlist("product"))):
            product_id = request.POST.getlist("product")[i]
            qty = int(request.POST.getlist("qty")[i])
            product = Product.objects.get(id=product_id)
            price = product.price
            tax = (price * product.tax_percent / 100) * qty
            line_total = (price * qty) + tax

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                qty=qty,
                price=price,
                tax_amount=tax,
                line_total=line_total,
            )

            total += (price * qty)
            tax_total += tax

        invoice.subtotal = total
        invoice.tax_total = tax_total
        invoice.grand_total = total + tax_total
        invoice.save()

        return redirect("invoice_detail", pk=invoice.pk)

    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, "billing/invoice_create.html", {"customers": customers, "products": products})

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "billing/invoice_detail.html", {"invoice": invoice})
