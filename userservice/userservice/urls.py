from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('userservice/', include('api.urls')),
    
    # monitoring
    path('', include('django_prometheus.urls')),
]
