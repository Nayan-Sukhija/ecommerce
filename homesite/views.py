from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Cart, CartItem, Order, OrderItem, Category
from .decorators import redirect_if_not_logged_in
from userlogin.models import UserProfile
from .functions import *

def home(request):
    products = Product.objects.all()
    context = {
            "products": products,
        }
    print(request.user.is_superuser)
    return render(request, 'homesite\\html\\home.html', context=context)


@redirect_if_not_logged_in
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')

@redirect_if_not_logged_in
def remove_cart(request, cartitem_id):
    previous_url = request.META.get('HTTP_REFERER', '/')
    CartItem.objects.get(id=cartitem_id).delete()
    return redirect(previous_url)


def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    items = {}
    for item in cart_items:
        items[item.product.name] = {
            'quantity': item.quantity,
            'total_price': item.quantity*item.product.discounted_price,
            'id': item.product.id
        }
    context = {
        'cart': cart, 
        'items': items,
    }
    return render(request, 'homesite\\html\\view_cart.html', context)

def product_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    discount = int(product.main_price) - int(product.discounted_price)
    percent = round(discount*100 / int(product.main_price))
    context = {
        'product': product, 
        'img_count': Product.get_image_range(product),
        'percent': percent,
    }
    return render(request, 'homesite\\html\\product_page.html', context=context)


@redirect_if_not_logged_in
def add_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    size = request.POST.get('size')
    is_cartitem = CartItem.objects.filter(cart=cart, product=product, size=size).first()
    if is_cartitem is not None:
        is_cartitem.quantity = int(request.POST.get('quantity')) + int(is_cartitem.quantity)
        is_cartitem.save()
    else:
        quantity = request.POST.get('quantity')
        CartItem.objects.create(product=product, cart=cart, quantity=quantity, size=size)
    product_id = request.POST.get('product_id')
    url = reverse('product_page', args=[product_id])
    return redirect(url)



def buy_now(request):
    product_id = request.GET.get('product_id')
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        size = request.POST.get('size')
        is_cartitem = CartItem.objects.filter(cart=cart, product=product, size=size).first()
        if is_cartitem is not None:
            is_cartitem.quantity = int(request.POST.get('quantity')) + int(is_cartitem.quantity)
            is_cartitem.save()
        else:
            quantity = request.POST.get('quantity')
            CartItem.objects.create(product=product, cart=cart, quantity=quantity, size=size)
    return checkout_page(request)



def checkout_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        cart_items_list = [
            {
                'id': item.id,
                'discounted_price': item.product.discounted_price * item.quantity,
                'main_price': item.product.main_price,
                'quantity': item.quantity,
                'name': item.product.name,
                'size': item.size,
            } 
            for item in cart_items
        ]
        total = 0
        for item in cart_items_list:
            total += item['discounted_price']

        context = {
            "cart_items_list": cart_items_list,
            "total": total
        }
    else:
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        total = int(product.discounted_price)*int(quantity)
        cart_items_list = {
                'id': product.id,
                'discounted_price': total,
                'quantity': quantity,
                'name': product.name,
                'size': size,
            }
        context = {
            "cart_items_list": cart_items_list,
            "total": total
        }
    return render(request, 'homesite\\html\\checkout.html', context=context)


def pay_now(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')

        # payment gateway API success
        order_no = generate_order_no()
        order = Order.objects.create(user=request.user, order_no=order_no, status=0)
        for item in cart_items:
            price = int(item.product.discounted_price)*int(item.quantity)
            OrderItem.objects.create(product=item.product, order=order, quantity=item.quantity, size=item.size, price=price)
        cart_items.delete()
        return redirect('home')
    else:
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        size = request.GET.get('size')
        quantity = request.GET.get('quantity')
        price = int(quantity)*int(product.discounted_price)

        # payment gateway API success

        user = UserProfile.objects.get(email='nayansukhija@gmail.com')
        order_no = generate_order_no()
        order = Order.objects.create(user=user, order_no=order_no, status=0)
        OrderItem.objects.create(product=product, order=order, quantity=quantity, size=size)
        return redirect('home')
    

def get_categories(request):
    if request.GET.get('gender') == 'women':
        category = Category.objects.filter(for_women=True)
    elif request.GET.get('gender') == 'men':
        category = Category.objects.filter(for_men=True)
    context = {
        'category': category
    }
    print(context)
    return render(request, 'homesite\\html\\category.html', context=context)