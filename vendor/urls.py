from django.urls import path
from . import views


urlpatterns = [
    path('',views.vendor_login, name='vendor_login'),
    path('vendor_logout/',views.vendor_logout, name='vendor_logout'),
    path('vendor_home/',views.vendor_home, name='vendor_home'),

    path('vendor_register/', views.vendor_register, name='vendor_register'),
    path('activate/<uidb64>/<token>/', views.activate, name='vendoractivate'),

    path('forgotpassword/', views.vendor_forgot_password, name='vendor_forgotpassword'),
    path('vendor_resetpassword/<uidb64>/<token>/', views.vendor_resetpassword_validate, name='vendor_resetpassword_validate'),
    path('vendor_resetpasswordpage/',views.vendor_resetpasswordpage, name='vendor_resetpasswordpage'),
    
    path('viewproduct/<int:id>', views.viewproduct, name='viewproduct'),
    path('editproduct/<str:slug>', views.editproduct, name='editproduct'),
    path('addproduct',views.add_product,name='addproduct'),
    path('unlist_product/<int:id>',views.unlist_product, name='unlist_product'),
    path('view_unlisted_product/<int:id>', views.view_unlisted_product, name='view_unlisted_product'),

    path('product_order/', views.product_order, name='product_order'),
    path('canceldproduct_order/', views.canceld_product_order, name='canceld_order'),
    path('soldproduct_list/', views.soldproduct_list, name='soldproduct_list'),

    
]


