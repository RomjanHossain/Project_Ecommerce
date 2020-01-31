from django.urls import path
from . import views
urlpatterns = [
    path('test/', views.ProductView, name='product'),
    path('detail/<slug:slug>', views.DeatilView, name='detail'),
    path('quick/<slug:slug>', views.QuickView, name='qv'),
]
