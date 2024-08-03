from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('remove_cart/<int:cartitem_id>/', remove_cart, name='remove_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('product/<int:product_id>/', product_page, name='product_page'), 
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'), 
    path('checkout/', checkout_page, name='checkout'),
    path('buy_now/', buy_now, name='buy_now'),
    path('pay_now/', pay_now, name='pay_now'),
    path('get_categories/', get_categories, name='get_categories'),
]