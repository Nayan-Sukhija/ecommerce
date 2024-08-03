from django.urls import path, include
from .views import register, user_login, user_logout, user_account, user_address, add_address

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('user_address/', user_address, name='user_address'),
    path('add_address/', add_address, name='add_address'),
    path('account/', user_account, name='user_account'),
]