from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product, Customer, Purchase, Sale, Inventory, SaleItem
from django import forms
from django.db import transaction
from django.db import models
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
        form = VendorForm(request.POST, request.FILES)
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
        form = VendorForm(request.POST, request.FILES, instance=vendor)
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
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:product_list')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})


def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('main:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_update.html', {'form': form, 'product': product})


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('main:product_list')
    return render(request, 'product_delete.html', {'product': product})


def customer_list(request):
    customers = Customer.objects.filter(vendor=request.user)
    return render(request, 'customer_list.html', {'customers': customers})


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, vendor=request.user)
    return render(request, 'customer_detail.html', {'customer': customer})


def customer_create(request):
    if request.method == 'POST':
        customer_data = request.POST.copy()  # Make a copy of the POST data
        errors = {}  # To store any validation errors
        print(customer_data)
        print(errors)

        # Perform manual form validation
        required_fields = ['customer_name', 'customer_address', 'customer_mobile' ]  # Define the required fields
        for field in required_fields:
            if not customer_data.get(field):
                errors[field] = f"{field.capitalize()} field is required."

        if not errors:
            # Create the customer object and set the vendor
            customer = Customer.objects.create(
                customer_name=customer_data['customer_name'],
                customer_address=customer_data['customer_address'],
                customer_mobile=customer_data['customer_mobile'],
                vendor=request.user,
                
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


def purchase_list(request):
    purchases = Purchase.objects.filter(vendor__user=request.user)
    return render(request, 'purchase_list.html', {'purchases': purchases})


def purchase_detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, vendor__user=request.user)
    return render(request, 'purchase_detail.html', {'purchase': purchase})


def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            return redirect('main:purchase_detail', purchase_id=purchase.id)
    else:
        form = PurchaseForm()
    return render(request, 'purchase_create.html', {'form': form})


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
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor=request.user)
    sale_items = SaleItem.objects.filter(sale=sale)
    return render(request, 'sale_detail.html', {'sale': sale, 'sale_items': sale_items})


@login_required
def sale_create(request):
    products = Inventory.objects.filter(vendor=request.user.vendor_profile)
    customers = Customer.objects.filter(vendor=request.user)

    if request.method == 'POST':
        errors = {}
        sale_items = []

        customer_id = request.POST.get('customer')
        
        
        if not customer_id:
            errors['customer'] = 'Customer field is required.'

        product_ids = request.POST.getlist('product[]')
        quantities = request.POST.getlist('qty[]')
        prices = request.POST.getlist('price[]')
        

        print(product_ids, quantities)

        for product_id, quantity,price in zip(product_ids, quantities,prices):
            if not product_id:
                errors['product'] = 'Product field is required.'
            elif not quantity:
                errors['qty'] = 'Quantity field is required.'
            elif not price:
                errors['price'] = 'Price field is required.'
            else:
                try:
                    quantity = int(quantity)
                    price = int(price)


                    if quantity <= 0 or price <= 0 :
                        errors['qty'] = 'Quantity must be a positive integer.'
                        errors['price'] = 'Price must be a positive integer.'
                except ValueError:
                    errors['qty'] = 'Quantity must be a valid integer.'
                    errors['price'] = 'Price must be a valid integer.'

            if not errors.get('product') and not errors.get('qty') and not errors.get('price') :
                try:
                    product = Product.objects.get(id=product_id)
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
                        SaleItem.objects.create(sale=sale, product=product, qty=quantity, price=price)

                    # Trigger bill generation for the created sale
                    bill_generation(request, sale.id)

                return redirect('main:sale_detail', sale_id=sale.id)
            except Customer.DoesNotExist:
                errors['customer'] = 'Invalid customer.'

        return render(request, 'sale_create.html', {'errors': errors, 'products': products, 'customers': customers})

    return render(request, 'sale_create.html', {'products': products, 'customers': customers})


@login_required
def sale_update(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor=request.user)
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
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor=request.user)
    if request.method == 'POST':
        sale.delete()
        return redirect('main:sale_list')
    return render(request, 'sale_delete.html', {'sale': sale})

import xhtml2pdf.pisa as pisa

from django.http import HttpResponse

from django.template.loader import get_template
from django.template import Context
from reportlab.pdfgen import canvas
from io import BytesIO


def bill_generation(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor=request.user)

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
        quantity = item.qty //2
        inventory = Inventory.objects.get(product=product, vendor=request.user.vendor_profile)
        inventory.total_bal_qty = inventory.total_bal_qty - quantity
        print(quantity, inventory.total_bal_qty)
        inventory.save()

    # Render the bill template with the sale and line items information
    

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from reportlab.pdfgen import canvas


def bill_generate_pdf(request, sale_id):
    # Get the sale object
    sale = get_object_or_404(Sale, id=sale_id, customer__vendor=request.user)

    # Calculate the total price for each product in the sale
    line_items = []
    total_price = 0
    grandtotal = 0
    for item in sale.sale_items.all():
        product = item.product
        quantity = item.qty
        price = item.price * quantity
        line_items.append({
            'product': product,
            'quantity': quantity,
            'price': price/quantity,
            'total_price':  price
        })
        print(price, quantity, quantity * price, grandtotal)
        grandtotal +=  price 

    # Generate PDF bill
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)

    # Set up PDF content
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Bill Details")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, f"Sale ID: {sale.id}")
    pdf.drawString(100, 680, f"Customer: {sale.customer}")
    pdf.drawString(100, 660, f"Vendor: {sale.vendor}")
    pdf.drawString(100, 640, f"Sale Date: {sale.sale_date}")
    pdf.drawString(100, 620, f"Product \t Quantity \t Price \t Total Price")

    # Draw line items
    y = 600
    for item in line_items:
        pdf.drawString(100, y, f"{item['product']} \t {item['quantity']} \t {item['price']} \t {item['total_price']}")
        y -= 20

    pdf.drawString(100, y-40, f"Total Price: {grandtotal}")

    # Save PDF to buffer
    pdf.showPage()
    pdf.save()
    pdf_buffer.seek(0)

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