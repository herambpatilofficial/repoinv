# Generated by Django 3.2.4 on 2023-06-30 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20230630_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock_qty',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
    ]
