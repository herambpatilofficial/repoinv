from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('vendor/', views.vendor_list, name='vendor_list'),
    path('vendor/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('vendor/create/', views.vendor_create, name='vendor_create'),
    path('vendor/update/<int:vendor_id>/', views.vendor_update, name='vendor_update'),
    path('vendor/delete/<int:vendor_id>/', views.vendor_delete, name='vendor_delete'),
    path('product/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/update/<int:product_id>/', views.product_update, name='product_update'),
    path('product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('customer/', views.customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customer/create/', login_required(views.customer_create), name='customer_create'),
    path('customer/update/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('customer/delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('purchase/', views.purchase_list, name='purchase_list'),
    path('purchase/<int:purchase_id>/', views.purchase_detail, name='purchase_detail'),
    path('purchase/create/', views.purchase_create, name='purchase_create'),
    path('purchase/update/<int:purchase_id>/', views.purchase_update, name='purchase_update'),
    path('purchase/delete/<int:purchase_id>/', views.purchase_delete, name='purchase_delete'),
    path('sale/', views.sale_list, name='sale_list'),
    path('sale/<int:sale_id>/', views.sale_detail, name='sale_detail'),
    path('sale/create/', views.sale_create, name='sale_create'),
    path('sale/update/<int:sale_id>/', views.sale_update, name='sale_update'),
    path('sale/delete/<int:sale_id>/', views.sale_delete, name='sale_delete'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:inventory_id>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    path('inventory/update/<int:inventory_id>/', views.inventory_update, name='inventory_update'),
    path('inventory/delete/<int:inventory_id>/', views.inventory_delete, name='inventory_delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # url for billing
    path('bill_generation/<int:sale_id>/', views.bill_generate_pdf, name='bill_generation'),
    # Urls for export to excel

    path('export_vendors_csv', views.export_vendors_csv, name='export_vendors_csv'),
    path('export_products_csv', views.export_products_csv, name='export_products_csv'),
    path('export_customers_csv', views.export_customers_csv, name='export_customers_csv'),
    path('export_purchases_csv', views.export_purchases_csv, name='export_purchases_csv'),
    path('export_sales_csv', views.export_sales_csv, name='export_sales_csv'),
    path('export_inventories_csv', views.export_inventories_csv, name='export_inventories_csv'),
    #

    
    ]
