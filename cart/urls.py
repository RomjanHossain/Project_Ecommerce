from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('up/', views.cart_update, name='update'),
]
