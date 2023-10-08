from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('', views.get_routes, name='get_routes'),

    path('users/register/', views.register_user, name='register'),

    path('users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile', views.get_user_profile, name='get_user_profile'),
    path('users/', views.get_users, name='users'),
     
    path('get_products/', views.get_products, name='get_products'),
    path('get_the_product/<str:pk>/', views.get_the_product, name='get_the_product'),
]