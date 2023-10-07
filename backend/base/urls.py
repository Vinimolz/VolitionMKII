from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('get_products/', views.get_products, name='get_products'),
    path('get_the_product/<str:pk>/', views.get_the_product, name='get_the_product'),
]