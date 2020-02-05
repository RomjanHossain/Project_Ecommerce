from django.urls import path
from . import views
urlpatterns = [
    path('checkoutform', views.checkout_address_create_view, name="checkoutaddview"),
    path('addreuse/', views.checkout_address_reuse_view, name='reuse'),
]
