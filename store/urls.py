from django.urls import path
from.views import (
    store,
    checkout,
    cart

)
urlpatterns = [
    path('',store,name='store'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
]
