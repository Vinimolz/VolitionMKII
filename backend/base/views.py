from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from .serializer import ProductSerializer, UserSerializer, UserSerializerWithToken

from .models import Product

from .products import products

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():
            data[key] = value

        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def get_routes(request):

    routes = [
        '/api/products',
        '/api/products/create',
        '/api/products/upload',
        '/api/products/<id>/reviews',
        '/api/products/top',
        '/api/products/<id>',
        '/api/products/delete/<id>',
        '/api/products/<update>/<id>',
    ]

    return Response(routes)

@api_view(['POST'])
def register_user(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail' : 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_the_product(request, pk):

    product = Product.objects.get(_id=pk)
    
    serializer = ProductSerializer(product, many=False)
    
    return Response(serializer.data)
