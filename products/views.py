from django.shortcuts import render
from .models import Product, Brand
from django.core.paginator import Paginator

# Create your views here.


def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(brand__name__icontains=query) if query else Product.objects.all()
    brands = Product.objects.values_list('brand__name', flat=True).distinct()

    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'query': query
    }
    return render(request, 'products/product_list.html', context)
