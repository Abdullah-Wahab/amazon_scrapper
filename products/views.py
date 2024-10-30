from django.shortcuts import render
from .models import Product, Brand

# Create your views here.


def product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    products = brand.products.all()
    return render(request, 'products/product_list.html', {'brand': brand, 'products': products})
