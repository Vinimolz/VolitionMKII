from django.urls import path
from base.views import product_views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [     
    path('', views.get_products, name='get_products'),
    path('create/', views.create_product, name='create_product'),
    path('<str:pk>/', views.get_the_product, name='get_the_product'),
    path('delete/<str:pk>/', views.delete_product, name='delete_product'),
    path('update/<str:pk>/', views.update_product, name='update_product'),
    
]