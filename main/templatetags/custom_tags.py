# Custom tags.py

from django import template
from django.db.models import Sum
import requests
from main.views import customer_create

register = template.Library()

@register.inclusion_tag('main/customer_create.html')
def render_customer_form():
    form = customer_create()
    return {'form': form}
