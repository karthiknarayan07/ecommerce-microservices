from django.urls import path
from .views import *

urlpatterns = [
    # product apis
    path('products',ProductsView.as_view()),
]
