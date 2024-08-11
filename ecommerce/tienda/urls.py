from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',Home.as_view(),name='Home'),
    path('inicio',Home.as_view(),name='inicio'),
    path('checkout',Checkout.as_view(),name='checkouk'),
    path('detail',Detail.as_view(),name='detail'),
    path('shop',Shop.as_view(),name='shop'),
    path('contact',Contact.as_view(),name='contac'),
    path('detail/<int:pk>', Detail.as_view(), name='detail'),

]