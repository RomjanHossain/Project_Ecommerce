from django.urls import path
from . import views
urlpatterns = [
    path('search/', views.searchedView, name='search'),
    path('error/', views.error, name="error"),
]
