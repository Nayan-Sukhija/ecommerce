from .models import Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        cart_items_list = [
            {
                'id': item.id,
                'discounted_price': item.product.discounted_price * item.quantity,
                'main_price': item.product.main_price,
                'quantity': item.quantity,
                'productid': item.product.id,
                'name': item.product.name,
                'size': item.size,
            } 
            for item in cart_items
        ]
    else:
        cart_items_list = []
    return {'cart_items_list': cart_items_list}

def get_user_details(request):
    if request.user.is_authenticated:
        if request.user.is_staff == True:
            return {'staff': 'true'}
        else:
            return {'staff': 'false'}
    return {'staff': 'false'}