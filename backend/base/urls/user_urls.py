from django.urls import path
from base.views import user_views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('register/', views.register_user, name='register'),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('', views.get_users, name='users'),
]