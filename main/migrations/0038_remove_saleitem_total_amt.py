# Generated by Django 4.2.2 on 2023-08-03 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_productcategory_product_product_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitem',
            name='total_amt',
        ),
    ]
