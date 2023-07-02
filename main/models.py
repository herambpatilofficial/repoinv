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
    photo = models.ImageField(upload_to="vendor/")
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


class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="product/")

    class Meta:
        verbose_name_plural = '3. Products'

    def __str__(self):
        return self.title


class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True, default=" ")
    customer_mobile = models.CharField(max_length=50, default="0")
    customer_address = models.TextField(default=" ")
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers',default=1)

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name_plural = '7. Customers'


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    qty = models.FloatField()
    price = models.FloatField()
    total_amt = models.FloatField(default=0)
    pur_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Purchases'

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.price
        super(Purchase, self).save(*args, **kwargs)

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




class Sale(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    billed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Sales'


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='sale_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    price = models.FloatField(default=0)
    total_amt = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.price
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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


@receiver(post_delete, sender=Vendor)
def delete_vendor_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete()


@receiver(post_delete, sender=Product)
def delete_product_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete()
