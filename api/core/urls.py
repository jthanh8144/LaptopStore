from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('changepass/', changePassword, name='changePass'),
    path('updateuser/', updateUser, name='updateUser'),
    path('products/', products, name='products'),
    path('products/<str:code>/', detailProduct, name='detailProduct'),
    path('search/', searchProducts, name='searchProduct'),
]
