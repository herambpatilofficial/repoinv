from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


from .models import User, Vendor, Unit, Product, Purchase, Customer, Sale, Inventory, SaleItem


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Vendor info', {'fields': ('is_vendor',)}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_vendor')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_vendor')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'address', 'mobile', 'status')
    list_filter = ('status',)
    search_fields = ('full_name', 'user__username', 'user__email')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_name')
    model = Unit


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'detail', 'unit', 'photo')
    model = Product


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'qty', 'price', 'total_amt', 'pur_date')
    list_filter = ('pur_date','vendor')
    model = Purchase


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_mobile', 'customer_address', 'vendor')
    model = Customer


class SaleAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'customer', 'sale_date')
    model = Sale


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'pur_qty', 'sale_qty','total_bal_qty')
    list_filter = ('vendor', 'product')
    model = Inventory

class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'qty', 'price', 'total_amt')
    model = SaleItem

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(SaleItem)

