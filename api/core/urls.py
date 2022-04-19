from django.urls import path
from .views import *

urlpatterns = [
    path('user/register/', register, name='register'),
    path('user/login/', login, name='login'),
    path('user/logout/', logout, name='logout'),
    path('user/changepass/', changePassword, name='changePass'),
    path('user/updateuser/', updateUser, name='updateUser'),
    path('products/', products, name='products'),
    path('products/new/', newProducts, name='newProduct'),
    path('products/search/', searchProducts, name='searchProduct'),
    path('products/instock/', instockProducts, name='instockProduct'),
    path('products/hot/', hotProducts, name='hotProduct'),
    path('products/<str:code>/', detailProduct, name='detailProduct'),
    path('brand/', brand, name='brand'),
    
]
