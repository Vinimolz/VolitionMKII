from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status

from base.serializer import ProductSerializer
from base.models import Product, Review
from base.products import products

@api_view(['GET'])
def get_products(request):
    query = request.query_params.get('keyword')

    if query is None or query == '':
        query = ''
      
    products = Product.objects.filter(name__icontains=query)

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

@api_view(['POST'])
#@permission_classes([IsAdminUser])    
def upload_image(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_review(request, pk):

    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    alreadyExists = product.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail': 'Product review already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating for the review'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        review = Review.objects.create(
            user = user,
            product = product,
            name = user.first_name,
            rating = data['rating'],
            comment = data['comment']
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review was added successfully')
