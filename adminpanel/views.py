from django.shortcuts import render
from homesite.models import Order, OrderItem
from homesite.decorators import redirect_if_not_logged_in, redirect_if_not_admin

@redirect_if_not_logged_in
@redirect_if_not_admin
def adminPanel(request):
    orders_per_page = 5
    page_number = int(request.GET.get('page', 1))
    start_index = (page_number - 1) * orders_per_page
    end_index = start_index + orders_per_page
    orders = OrderItem.objects.select_related('order', 'product').all().order_by('-date_created')
    order_items_list = [
        {
            'order_no': item.order.order_no,
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
    return render(request, 'adminpanel\\html\\admin_panel.html', context=context)

def get_orders(request):
    pass




