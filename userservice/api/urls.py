from django.urls import path,include
from .views import *

urlpatterns = [
    path('test', TestView.as_view()),
    
    # auth apis
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
]