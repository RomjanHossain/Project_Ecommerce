from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # path('signin/', views.login_form, name='login'),
    path('signin/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    #    path('register/', views.register, name='regi'),
    path('register/', views.RegisterView.as_view(), name='regi'),
    path('guestf/', views.guestform, name='gf'),
    path('success/', views.SuccessPage, name='success'),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
