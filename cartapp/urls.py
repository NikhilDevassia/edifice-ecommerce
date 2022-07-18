from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('addcart/<int:product_id>', views.add_cart, name='addcart'),
    path('removecart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name='removecart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('coupon_page/', views.coupon_page, name='coupon_page')
]
 