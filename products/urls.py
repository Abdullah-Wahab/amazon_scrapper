from django.urls import path
from .views import product_list

urlpatterns = [
    path('brand/<int:brand_id>/products/', product_list, name='product_list'),
]
