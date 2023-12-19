from django.urls import path,include
from .views import *
from .s2s_views import *

urlpatterns = [
    path('test', TestView.as_view()),
    
    # authentication apis
    path('register',RegisterView.as_view()),
    path('register/superadmin',SuperAdminRegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('profile',ProfileView.as_view()),
    
    # server to server apis
    path('internal/user',UserView.as_view()),
]