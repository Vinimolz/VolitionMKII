from django.urls import path
from base.views import product_views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [     
    path('', views.get_products, name='get_products'),
    path('<str:pk>/', views.get_the_product, name='get_the_product'),
]