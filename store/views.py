from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartData,cookieCart
def store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)
def cart(request):
    data=cartData(request)
    cartItems=data['cartItems']
    items=data['items']
    order=data['order']

    context={'items':items,
            'order':order,
            'cartItems':cartItems
            }
    return render(request,'store/cart.html',context)
def checkout(request):
    data=cartData(request)
    cartItems=data['cartItems']
    items=data['items']
    order=data['order']

    context={'items':items,
            'order':order,
            'cartItems':cartItems
            }
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('Action:',action)
    print('productId:',productId)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderitem.quantity+=1
    elif action=='remove':
        orderitem.quantity-=1
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    return JsonResponse('Item was added', safe=False)
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'].replace(',',''))
        order.transaction_id=transaction_id
        print(total)
        print(order.get_cart_total)
        if total==order.get_cart_total:
            order.complete=True
        order.save()
        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                state=data['shipping']['state'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],

            )

    else:
        print('User is not logged in')
    return JsonResponse('Payment complete',safe=False)
# Create your views here.
