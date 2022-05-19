from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import Product_Form
from .forms import User_Form
from django.http import JsonResponse
import json


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
    #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    customers = Customer.objects.all()
    products = Product.objects.all()
    context = {'products':products, 'customers':customers, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
    #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
    #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def room(request):
    return render(request, 'store/room.html')

def product(request):
#if request.POST.get('pname') and request.POST.get('price') and request.POST.get('pdescription') and (request.POST.get('digital') or request.POST.get('notdigital')) and request.POST.get('pimage'):
    if request.method == 'POST':
        form = Product_Form(request.POST, request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            newProduct=Product()
            newProduct.name= form.cleaned_data["name"]
            newProduct.price= form.cleaned_data["price"]
            newProduct.description= form.cleaned_data["description"]
            newProduct.digital = form.cleaned_data["digital"] == 'Digital'
            newProduct.image= form.cleaned_data["image"]
            newProduct.save()
        return HttpResponseRedirect('/')
    else:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
      products = Product.objects.all()
      form = Product_Form()
      context = {'products':products, 'form':form, 'cartItems':cartItems}
      return render(request, 'store/product.html', context)

def user(request):
    if request.method == 'POST':
        form = User_Form(request.POST)
        if form.is_valid():
            newUser = Customer()
            newUser.name= form.cleaned_data["name"]
            newUser.email= form.cleaned_data["email"]
            newUser.save()
        return HttpResponseRedirect('/')
    else:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
      form = User_Form()
      context = {'form':form, 'cartItems':cartItems}
      return render(request, 'store/user.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
