from django.test import TestCase, Client
from django.urls import reverse
from main.models import Vendor, Product, Customer, Purchase, Sale, Inventory, SaleItem

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.product = Product.objects.create(name='Test Product')
        self.customer = Customer.objects.create(name='Test Customer', vendor=self.vendor)
        self.purchase = Purchase.objects.create(vendor=self.vendor)
        self.sale = Sale.objects.create(customer=self.customer)

    def test_vendor_list(self):
        response = self.client.get(reverse('vendor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendor_list.html')

    def test_vendor_detail(self):
        response = self.client.get(reverse('vendor_detail', args=[self.vendor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendor_detail.html')

    # Add more test methods for other views...

    def test_sale_list(self):
        response = self.client.get(reverse('sale_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale_list.html')

    def test_sale_detail(self):
        response = self.client.get(reverse('sale_detail', args=[self.sale.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale_detail.html')

    def test_sale_create(self):
        response = self.client.get(reverse('sale_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale_create.html')

    # Add more test methods for other views...

