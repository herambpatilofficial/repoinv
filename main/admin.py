from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Vendor)
admin.site.register(models.Unit)
# admin.site.register(models.Franchisee)

class CustomerAdmin(admin.ModelAdmin):
    search_fields=['customer_name','customer_mobile']
    list_display=['customer_name','customer_mobile']
admin.site.register(models.Customer,CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit']
admin.site.register(models.Product,ProductAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display=['id','product','qty','price','total_amt','vendor','pur_date']
    search_fields=['product__title','product__unit__title']
admin.site.register(models.Purchase,PurchaseAdmin)


class InventoryAdmin(admin.ModelAdmin):
    search_fields=['product__title','product__unit__title']
    list_display=['product','pur_qty','sale_qty','total_bal_qty','product_unit','pur_date','sale_date']

admin.site.register(models.Inventory,InventoryAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display=['id','customer','product','qty','price','total_amt','sale_date']
    search_fields=['product__title','product__unit__title']
admin.site.register(models.Sale,SaleAdmin)