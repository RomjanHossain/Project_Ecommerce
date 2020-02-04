from django.urls import path
from . import views
urlpatterns = [
    path('conform/', views.ConformOrder, name='ConformO'),
]
