from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product, Customer, Purchase, Sale, Inventory, SaleItem, Unit
from django import forms
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect


# Home view

def home(request):
    return render(request, 'home.html')



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'


from django.forms import inlineformset_factory

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})


def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    return render(request, 'vendor_detail.html', {'vendor': vendor})


def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('main:vendor_list')
    else:
        form = VendorForm()
    return render(request, 'vendor_create.html', {'form': form})


def vendor_update(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('main:vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor_update.html', {'form': form, 'vendor': vendor})


def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        vendor.delete()
        return redirect('main:vendor_list')
    return render(request, 'vendor_delete.html', {'vendor': vendor})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def product_create(request):
    units = Unit.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:product_list')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form, 'units': units})


def product_update(request, product_id):
    units = Unit.objects.all()
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('main:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_update.html', {'form': form, 'product': product, 'units': units})


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('main:product_list')
    return render(request, 'product_delete.html', {'product': product})


def customer_list(request):
    if request.user.is_superuser:
        customers = Customer.objects.all()
    else:
        customers = Customer.objects.filter(vendor=request.user)
        
    return render(request, 'customer_list.html', {'customers': customers})


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, vendor__user=request.user)
    return render(request, 'customer_detail.html', {'customer': customer})


def customer_create(request):
    if request.method == 'POST':
        customer_data = request.POST.copy()  # Make a copy of the POST data
        errors = {}  # To store any validation errors
        print(customer_data)
        print(errors)

        # Perform manual form validation
        required_fields = ['customer_name', 'customer_address', 'customer_mobile']  # Define the required fields
        for field in required_fields:
            if not customer_data.get(field):
                errors[field] = f"{field.capitalize()} field is required."

        if not errors:
            # Create the customer object and set the vendor
            customer = Customer.objects.create(
                customer_name=customer_data['customer_name'],
                customer_address=customer_data['customer_address'],
                customer_mobile=customer_data['customer_mobile'],
                vendor=request.user
            )

            return redirect('main:customer_list')
    else:
        errors = {}
        customer_data = {}

    return render(request, 'customer_create.html', {'errors': errors, 'customer_data': customer_data})


def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, vendor=request.user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('main:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_update.html', {'form': form, 'customer': customer})


def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, vendor=request.user)
    if request.method == 'POST':
        customer.delete()
        return redirect('main:customer_list')
    return render(request, 'customer_delete.html', {'customer': customer})

@ login_required
def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase_list.html', {'purchases': purchases})


def purchase_detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, vendor__user=request.user)
    return render(request, 'purchase_detail.html', {'purchase': purchase})


def purchase_create(request):
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    if request.method == 'POST':
        
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # print form data in terminal
            print(form.cleaned_data)
            purchase = form.save()
            return redirect('main:purchase_list')
        else:
            print(form.errors)
    else:
        form = PurchaseForm()
    return render(request, 'purchase_create.html', {'form': form, 'products': products, 'vendors': vendors})


def purchase_update(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, vendor__user=request.user)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('main:purchase_detail', purchase_id=purchase.id)
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'purchase_update.html', {'form': form, 'purchase': purchase})


def purchase_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, vendor__user=request.user)
    if request.method == 'POST':
        purchase.delete()
        return redirect('main:purchase_list')
    return render(request, 'purchase_delete.html', {'purchase': purchase})


def sale_list(request):
    if request.user.is_superuser:
        sales = Sale.objects.all()
    else:
        sales = Sale.objects.filter(customer__vendor=request.user)
    selected_customer = request.GET.get('customer')

    # Filter sales based on the selected customer if it's not empty
    if selected_customer:
        sales = Sale.objects.filter(customer_id=selected_customer).order_by('-sale_date')
    else:
        sales = Sale.objects.all().order_by('-sale_date')

    # Pagination
    paginator = Paginator(sales, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all customers for the filter dropdown
    customers = Customer.objects.all()

    context = {
        'sales': page_obj,
        'customers': customers,
        'selected_customer': selected_customer
    }

    return render(request, 'sale_list.html', context)


def sale_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale_items = SaleItem.objects.filter(sale=sale)
    return render(request, 'sale_detail.html', {'sale': sale, 'sale_items': sale_items})


@login_required

def sale_create(request):
    # Get products in inventory for the current vendor
    products = Product.objects.filter(inventory__vendor=request.user.vendor_profile)
    customers = Customer.objects.filter(vendor=request.user)

    if request.method == 'POST':
        errors = {}
        sale_items = []
        total_price = 0.0

        customer_id = request.POST.get('customer')

        if not customer_id:
            errors['customer'] = 'Customer field is required.'

        product_ids = request.POST.getlist('product[]')
        quantities = request.POST.getlist('qty[]')
        prices = request.POST.getlist('price[]')

        for product_id, quantity, price in zip(product_ids, quantities, prices):
            if not product_id:
                errors['product'] = 'Product field is required.'
            elif not quantity:
                errors['qty'] = 'Quantity field is required.'
            elif not price:
                errors['price'] = 'Price field is required.'
            else:
                try:
                    quantity = int(quantity)
                    price = float(price)

                    if quantity <= 0 or price <= 0:
                        errors['qty'] = 'Quantity must be a positive integer.'
                        errors['price'] = 'Price must be a positive number.'
                    else:
                        total_price += quantity * price
                except ValueError:
                    errors['qty'] = 'Quantity must be a valid integer.'
                    errors['price'] = 'Price must be a valid number.'

            if not errors.get('product') and not errors.get('qty') and not errors.get('price'):
                try:
                    product = get_object_or_404(Product, id=product_id, inventory__vendor=request.user.vendor_profile)
                    sale_items.append({
                        'product': product,
                        'quantity': quantity,
                        'price': price
                    })
                except Product.DoesNotExist:
                    errors['product'] = 'Invalid product.'

        if not errors:
            try:
                customer = get_object_or_404(Customer, id=customer_id, vendor=request.user)

                with transaction.atomic():
                    sale = Sale.objects.create(customer=customer)

                    for sale_item in sale_items:
                        product = sale_item['product']
                        quantity = sale_item['quantity']
                        price = sale_item['price']
                        SaleItem.objects.create(sale=sale, product=product, qty=quantity)

                return redirect('main:sale_detail', sale_id=sale.id)
            except Customer.DoesNotExist:
                errors['customer'] = 'Invalid customer.'

        return render(request, 'sale_create.html', {'errors': errors, 'products': products, 'customers': customers})

    return render(request, 'sale_create.html', {'products': products, 'customers': customers})


@login_required
def sale_update(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor__user=request.user)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('main:sale_detail', sale_id=sale.id)
    else:
        form = SaleForm(instance=sale)
    return render(request, 'sale_update.html', {'form': form, 'sale': sale})


@login_required
def sale_delete(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor__user=request.user)
    if request.method == 'POST':
        sale.delete()
        return redirect('main:sale_list')
    return render(request, 'sale_delete.html', {'sale': sale})


import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from reportlab.pdfgen import canvas


def bill_generation(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor__user=request.user)

    if sale.billed:
        # The bill is already generated, redirect to the sale detail page
        return redirect('main:sale_detail', sale_id=sale.id)

    # Calculate the total price for each product in the sale
    line_items = []
    total_price = 0
    for item in sale.sale_items.all():
        product = item.product
        quantity = item.qty
        price = item.price * quantity
        line_items.append({
            'product': product,
            'quantity': quantity,
            'price': price
        })
        total_price += price

    # Update the sale status and save it
    sale.billed = True
    sale.save()

    # Update inventory quantities based on the sale
    for item in sale.sale_items.all():
        product = item.product
        quantity = item.qty
        inventory = Inventory.objects.get(product=product, vendor=request.user.vendor_profile)
        inventory.quantity -= quantity
        inventory.save()

    # Render the bill template with the sale and line items information
    template = get_template('bill.html')
    context = {
        'sale': sale,
        'line_items': line_items,
        'total_price': total_price
    }
    html = template.render(context)

    # Create a PDF file
    pdf_buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("ISO-8859-1")), pdf_buffer)

    # Set the response content type and headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bill.pdf"'

    # Write the PDF file to the response
    response.write(pdf_buffer.getvalue())

    return response

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from reportlab.pdfgen import canvas


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.lib.pagesizes import A4, A5, A6, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pytz
def bill_generate_pdf(request, sale_id):
    # Get the sale object
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor=request.user)

    # Calculate the total price for each product in the sale
    line_items = []
    grand_total = 0
    for item in sale.sale_items.all():
        product = item.product
        quantity = item.qty
        price = item.product.price * quantity
        line_items.append({
            'product': product,
            'quantity': quantity,
            'price': price / quantity,
            'total_price': price
        })

        grand_total += price

    # Set up PDF document
    # Set up PDF document
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.alignment = 1  # Center alignment
    title_style.fontSize = 22
    subtitle_style = ParagraphStyle("subtitle", parent=styles["Heading1"], fontSize=14)
    subtitle_style.alignment = 1  # Center alignment
    subtitle_style.fontSize = 18
    subtitle_style.spaceAfter = 0.5 * subtitle_style.fontSize
    header_style = styles["Heading3"]
    header_style.alignment = 1  # Center alignment
    table_header_style = styles["Heading4"]
    table_header_style.alignment = 1  # Center alignment
    table_data_style = styles["Normal"]
    table_data_style.alignment = 1  # Center alignment
    table_data_style.fontSize = 15
    table_data_style.spaceAfter = 0.5 * table_data_style.fontSize

    # Build PDF content
    content = []

    separator_line = Paragraph('<u>' + "_" * 40 + '</u>', table_data_style)

    content.append(separator_line)

    # Title
    title = Paragraph("TRYAMBAKAM RUDRAKSH", title_style)
    content.append(title)

    # Phone number
    phone_number = Paragraph("Phone number: 8805244048", subtitle_style)
    content.append(phone_number)

    # Separator line
    
    content.append(separator_line)

    contente3 = f"Sale ID: {sale.id}"
    contente2 = f"Customer: {sale.customer}"
    contente1 = f"Vendor: {sale.vendor}"
    # convert sale date and time to IST format
    sale_date = sale.sale_date.astimezone(pytz.timezone('Asia/Kolkata'))
    contente0 = f"Sale Date: {sale_date}"

    

    content.append(Paragraph(contente3, table_data_style))
    content.append(Paragraph(contente2, table_data_style))
    content.append(Paragraph(contente1, table_data_style))
    content.append(Paragraph(contente0, table_data_style))

    content.append(separator_line)

    # Tax invoice
    tax_invoice = Paragraph("TAX INVOICE", header_style)
    content.append(tax_invoice)



    # Line items table
    table_data = [["Product", "Quantity", "Price", "Total Price"]]
    for item in line_items:
        table_data.append([
            str(item["product"]),
            str(item["quantity"]),
            str(item["price"]),
            str(item["total_price"])
        ])

    table_style = TableStyle([
        
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 17),
        ("BOTTOMPADDING", (0, 0),(-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        
        ("FONTSIZE", (0, 1), (-1, -1), 17),
        # Set margins to bottom of table 
        
    ])
    
    table = Table(table_data)
    table.setStyle(table_style)
    content.append(table)

    # content.append(separaStor_line)


    # Total Price
    content.append(separator_line)
    total_price = Paragraph(f"<b>Total Price:</b> {grand_total}", subtitle_style)
    content.append(total_price)

    # content.append(separator_line)


    # Thank you
    thank_you = Paragraph("Thank you", subtitle_style)
    content.append(thank_you)

    # Generate PDF
    pdf.build(content)

    # Set up response with PDF content for download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{sale_id}.pdf"'
    response.write(pdf_buffer.getvalue())

    

    return response



class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'


def inventory_list(request):
    # If user is superuser, show all inventory
    if request.user.is_superuser:
        inventory = Inventory.objects.all()
    else:
        inventory = Inventory.objects.filter(vendor=request.user.vendor_profile)
    return render(request, 'inventory_list.html', {'inventory': inventory})


def inventory_detail(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    return render(request, 'inventory_detail.html', {'inventory': inventory})


def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save()
            return redirect('main:inventory_detail', inventory_id=inventory.id)
    else:
        form = InventoryForm()
    return render(request, 'inventory_create.html', {'form': form})


def inventory_update(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('main:inventory_detail', inventory_id=inventory.id)
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory_update.html', {'form': form, 'inventory': inventory})


def inventory_delete(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory.delete()
        return redirect('main:inventory_list')
    return render(request, 'inventory_delete.html', {'inventory': inventory})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('main:login')


# Views to export data from all models to CSV files using the django-import-export library when the user is superuser

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.urls import reverse
from django.utils.encoding import smart_str
from import_export.admin import ExportMixin
from import_export import resources

# ... (existing code for models and resources)


class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


class PurchaseResource(resources.ModelResource):
    vendor = resources.Field(attribute='vendor__full_name')  # Access the full_name attribute of the related Vendor model
    product = resources.Field(attribute='product__title')  # Access the title attribute of the related Product model

    class Meta:
        model = Purchase


class SaleResource(resources.ModelResource):
    vendor = resources.Field(attribute='vendor__full_name')  # Access the full_name attribute of the related Vendor model
    customer = resources.Field(attribute='customer__customer_name')  # Access the customer_name attribute of the related Customer model

    class Meta:
        model = Sale


class SaleItemResource(resources.ModelResource):
    product = resources.Field(attribute='product__title')  # Access the title attribute of the related Product model

    class Meta:
        model = SaleItem


class InventoryResource(resources.ModelResource):
    vendor = resources.Field(attribute='vendor__full_name')  # Access the full_name attribute of the related Vendor model
    product = resources.Field(attribute='product__title')  # Access the title attribute of the related Product model

    class Meta:
        model = Inventory


# ... (existing code for views)


@staff_member_required
def export_vendors_csv(request):
    vendors_resource = VendorResource()
    dataset = vendors_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendors.csv"'
    return response

@staff_member_required
def export_products_csv(request):
    products_resource = ProductResource()
    dataset = products_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    return response

@staff_member_required
def export_customers_csv(request):
    customers_resource = CustomerResource()
    dataset = customers_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    return response

@staff_member_required
def export_purchases_csv(request):
    purchases_resource = PurchaseResource()
    dataset = purchases_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="purchases.csv"'
    return response

@staff_member_required
def export_sales_csv(request):
    sales_resource = SaleResource()
    dataset = sales_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'
    return response

@staff_member_required
def export_sale_items_csv(request):
    sale_items_resource = SaleItemResource()
    dataset = sale_items_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sale_items.csv"'
    return response

@staff_member_required
def export_inventories_csv(request):
    inventories_resource = InventoryResource()
    dataset = inventories_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventories.csv"'
    return response
