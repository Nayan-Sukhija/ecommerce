from django.urls import path
from .views import adminPanel

urlpatterns = [
    path('panel/', adminPanel, name='admin_panel'),
]