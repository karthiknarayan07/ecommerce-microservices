from django.urls import path,include
from .views import *

urlpatterns = [
    path('test', TestView.as_view()),
]