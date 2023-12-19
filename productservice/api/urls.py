from django.urls import path

from api.products.views import ProductsView, ReadProductsView
from api.orders.views import OrdersView

urlpatterns = [
    
    # product crud views
    path('products',ProductsView.as_view()),
    
    # product read views    
    path('products/view',ReadProductsView.as_view()),
    
    # order apis
    path('products/order',OrdersView.as_view()),
    
]
