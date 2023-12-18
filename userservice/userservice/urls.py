from django.contrib import admin
from django.urls import path,include

import threading
from conf.rabbit_receiver import user_queue_receiver

receiver_thread = threading.Thread(target=user_queue_receiver, daemon=True)
receiver_thread.start()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userservice/', include('api.urls')),
    
    # monitoring
    path('', include('django_prometheus.urls')),
]
