from django.urls import path,include

import threading
from conf.rabbit_receiver import product_queue_receiver

receiver_thread = threading.Thread(target=product_queue_receiver, daemon=True)
receiver_thread.start()

urlpatterns = [
    # monitoring
    path('', include('django_prometheus.urls')),
]
