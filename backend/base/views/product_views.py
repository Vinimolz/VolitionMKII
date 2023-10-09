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

