from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)

    class Meta:
        # Add this meta option to avoid clashes with reverse accessors
        swappable = 'AUTH_USER_MODEL'


class Vendor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='vendor_profile'
    )
    full_name = models.CharField(max_length=50)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '1. Vendors'

    def __str__(self):
        return self.full_name


class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '2. Units'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '8. Product Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    product_code = models.CharField(max_length=10, unique=True, default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = '3. Products'

    def __str__(self):
        return self.title


class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True, default=" ")
    customer_mobile = models.CharField(max_length=50, default="0")
    customer_address = models.TextField(default=" ")
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers', default=1)

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name_plural = '7. Customers'

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_purchases')
    qty = models.FloatField()
    # total_amt should be calculated automatically
    total_amt = models.FloatField(default=0)
    pur_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Purchases'

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.product.price
        super(Purchase, self).save(*args, **kwargs)
        self.total_amt = self.qty * self.product.price

        # Update inventory for the specific vendor and product
        inventory, created = Inventory.objects.get_or_create(product=self.product, vendor=self.vendor)
        inventory.pur_qty += self.qty
        inventory.total_bal_qty += self.qty
        inventory.save()

    def delete(self, *args, **kwargs):
        # Restore inventory on purchase deletion
        inventory = Inventory.objects.get(product=self.product, vendor=self.vendor)
        inventory.pur_qty -= self.qty
        inventory.total_bal_qty -= self.qty
        inventory.save()

        super(Purchase, self).delete(*args, **kwargs)


from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db import models
from django.db.models import F, Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Sale(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=0, related_name='customer_sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    billed = models.BooleanField(default=False)
    

    class Meta:
        verbose_name_plural = 'Sales'

    # New property for total sale amount (read-only)
    @property
    def total_sale_amount(self):
        tsa = 0
        for saleitem in self.sale_items.all():
            tsa = tsa + saleitem.qty * saleitem.product.price
        return tsa
             

        
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='sale_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    total_amt = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.product.price
        super().save(*args, **kwargs)

        # Update inventory for the specific vendor and product
        inventory = Inventory.objects.get(product=self.product, vendor=self.sale.vendor)
        inventory.sale_qty += self.qty
        inventory.total_bal_qty -= self.qty
        inventory.save()

    def delete(self, *args, **kwargs):
        # Restore inventory on sale item deletion
        inventory = Inventory.objects.get(product=self.product, vendor=self.sale.vendor)
        inventory.sale_qty -= self.qty
        inventory.total_bal_qty += self.qty
        inventory.save()

        super().delete(*args, **kwargs)


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_inventory')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=None, null=True)

    pur_qty = models.FloatField(default=0)
    sale_qty = models.FloatField(default=0)
    total_bal_qty = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = '6. Inventory'

    def product_unit(self):
        return self.product.unit.title

    def pur_date(self):
        purchase = Purchase.objects.filter(product=self.product, vendor=self.vendor).first()
        if purchase:
            return purchase.pur_date

    def sale_date(self):
        sale = Sale.objects.filter(product=self.product, vendor=self.vendor).first()
        if sale:
            return sale.sale_date


class Expense(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    detail = models.TextField()
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '7. Expenses'

    