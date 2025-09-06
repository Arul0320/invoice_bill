from django.http import HttpResponse
from .models import Invoice
from reportlab.pdfgen import canvas

def export_invoice_pdf(request, pk):
    invoice = Invoice.objects.get(pk=pk)  # 👈 now pk is used
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.invoice_no}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Invoice No: {invoice.invoice_no}")
    p.drawString(100, 780, f"Customer: {invoice.customer.name}")
    p.drawString(100, 760, f"Total: {invoice.grand_total}")
    p.showPage()
    p.save()

    return response
