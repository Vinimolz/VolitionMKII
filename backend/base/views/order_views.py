from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.serializer import ProductSerializer, OrderSerializer
from base.models import Product, Order, OrderItem, ShippingAddress
from base.products import products

from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail' : 'No order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice']
        )

        shipping = ShippingAddress.objects.create(
            order = order, 
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'],
        )

        for i in orderItems:
            product = Product.objects.get(_id = i['product'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['qty'],
                price = i['price'],
                image = product.image.url
            )

            product.countInStock -= item.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user

    try:
        order = Order.objects.get(_id=pk)

        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many = False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not autorized to view order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exists'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders_by_id(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])    
def update_order_to_paid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response('Order was paid')

