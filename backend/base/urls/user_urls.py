from django.urls import path
from base.views import user_views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('register/', views.register_user, name='register'),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('profile/update/', views.update_user_profile, name='user_profile_update'),

    path('', views.get_users, name='users'),

    path('delete/<str:pk>/', views.delete_user, name='delete_user'),

    path('<str:pk>/', views.get_users_by_id, name='get_user_by_id'),
    path('update/<str:pk>/', views.update_user, name='update_user'),
    
]