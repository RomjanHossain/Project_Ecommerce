from django.urls import path
from . import views
urlpatterns = [
    path('checkoutform', views.checkout_address_create_view, name="checkoutaddview"),
]
