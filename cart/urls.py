from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('api/cart/', views.cart_detail_api_view, name='api-cart'),
    path('up/', views.cart_update, name='update'),
    path('checkout/', views.CheckoutView, name='checkout'),
]
