from django.contrib import admin
from django.urls import path,include

import threading
from conf.rabbit_receiver import communication_queue_receiver

receiver_thread = threading.Thread(target=communication_queue_receiver, daemon=True)
receiver_thread.start()

urlpatterns = [
    # monitoring
    path('', include('django_prometheus.urls')),
]
