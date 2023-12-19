from django.urls import path,include

import threading
from conf.rabbit_receiver import order_queue_receiver

receiver_thread = threading.Thread(target=order_queue_receiver, daemon=True)
receiver_thread.start()

urlpatterns = [
    
    # order service api urls
    path('orderservice/', include('api.urls')),
    
    # monitoring
    path('', include('django_prometheus.urls')),
]
