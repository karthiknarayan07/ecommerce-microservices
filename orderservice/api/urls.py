from django.urls import path
from .views import OrdersView
from .s2s_views import OrdersView as S2SOrdersView

urlpatterns = [
    path('orders', OrdersView.as_view()),
    path('internal/orders', S2SOrdersView.as_view()),
]
