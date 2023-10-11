from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.serializer import ProductSerializer
from base.models import Product
from base.products import products

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_the_product(request, pk):

    try:
        product = Product.objects.get(_id=pk)
        
        serializer = ProductSerializer(product, many=False)
        
        return Response(serializer.data)
    except:
        message = {'detail' : 'Product does not exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, pk):
    try:
        product = Product.objects.get(_id=pk)        
        product.delete()  
        return Response('Product Deleted')
    
    except:
        message = {'detail' : 'Product does not exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):

    user = request.user

    try:
        product = Product.objects.create(
            user = user,
            name = 'Sample name',
            price = 0,
            brand = 'Sample brand',
            countInStock = 0,
            category = 'Sample Categoty',
            description = ''
        )
        
        serializer = ProductSerializer(product, many=False)        
        return Response(serializer.data)
    
    except:
        message = {'detail' : 'Could not create new product'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request, pk):

    data = request.data

    try:
        product = Product.objects.get(_id=pk)

        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.description = data['description']

        product.save()
        
        serializer = ProductSerializer(product, many=False)
        
        return Response(serializer.data)
    except:
        message = {'detail' : 'Product could not be updated'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)