from django.urls import path,include
from .views import *

urlpatterns = [
    path('test', TestView.as_view()),
    
    # minitoring
    # path('metrics/', Prometheus.as_view(), name='prometheus-metrics'),
]