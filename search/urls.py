from django.urls import path
from . import views
urlpatterns = [
    path('search/', views.searchedView, name='search'),
]
