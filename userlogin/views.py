from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from homesite.decorators import redirect_if_not_logged_in
from .forms import RegistrationForm, LoginForm, UserAddressForm
from homesite.models import Order, OrderItem
from .models import UserAddress

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # group = Group.objects.get(name='user')
            user = form.save()
            # user.groups.add(group)
            login(request, user)
            return redirect('home')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'userlogin\\html\\register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            login(request, user)
            return redirect('home')  # Redirect to home or any desired page
    else:
        form = LoginForm()
    return render(request, 'userlogin\\html\\login.html', {'form': form})
    

def user_logout(request):
    logout(request)
    return redirect('home')

@redirect_if_not_logged_in
def user_account(request):
    orders_per_page = 5
    page_number = int(request.GET.get('page', 1))
    start_index = (page_number - 1) * orders_per_page
    end_index = start_index + orders_per_page
    orders = OrderItem.objects.select_related('order', 'product').filter(order__user=request.user).order_by('-date_created')
    print(orders)
    order_items_list = [
        {
            'oeder_no': item.order.order_no,
            'discounted_price': item.product.discounted_price * item.quantity,
            'main_price': item.product.main_price,
            'quantity': item.quantity,
            'productid': item.product.id,
            'name': item.product.name,
            'size': item.size,
        
        } for item in orders
    ]
    total_orders = len(order_items_list)
    order_items_list = order_items_list[start_index:end_index]
    total_pages = (total_orders + orders_per_page - 1) // orders_per_page
    context = {
        'order_items_list': order_items_list,
        'page_number': page_number,
        'total_pages': total_pages,
    }
    return render(request, 'userlogin\\html\\account.html', context=context)

def user_address(request):
    if request.GET.get('address'):
        address_id = request.GET.get('address')
        UserAddress.objects.filter(id=address_id).delete()
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user_address = form.save(commit=False)
            user_address.user = request.user
            user_address.save()
    else:
        form = UserAddressForm()
    user = request.user
    all_address = UserAddress.objects.filter(user=user)
    context = {
        "addresses": all_address,
        "form": form
    }
    return render(request, 'userlogin\\html\\user_address.html', context=context)

def add_address(request):
    context = {}
    return render(request, 'userlogin\\html\\add_address.html', context=context)