from django.urls import path
from . import views
urlpatterns = [
    path('product/', views.ProductView, name='product'),
    path('detail/<pk>', views.DeatilView,  name='deatil'),
]
