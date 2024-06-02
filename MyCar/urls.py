from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('cars',views.cars,name='cars'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('user',views.user,name='user'),
    path('admin',views.admin,name='admin'),
    path('cart',views.cart,name='cart'),
    path('ausers',views.ausers,name='ausers'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('puchases',views.puchases,name='puchases'),
    path('regform',views.regform,name='regform'),
    path('loginform',views.loginform,name='loginform'),
    path('add_products',views.add_products,name='add_products'),
    path('purchase',views.purchase,name='purchase'),
    path('logout',views.logout,name='logout'),
    path('approve',views.approve,name='approve'),
]