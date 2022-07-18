from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login, name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('admin_home/',views.admin_home, name='adminhome'),
    path('admin_user/',views.admin_user_manage, name='admin_user'),
    path('block_user/<int:pk>',views.block_user, name='block_user'),
    path('unblock_user/<int:pk>',views.unblock_user, name='unblock_user'),

    path('admin_vendor_manage/', views.admin_vendor_manage, name='admin_vendor_manage'),
    path('unblock_vendor/<int:pk>',views.unblock_vendor,name='unblock_vendor'),
    path('block_vendor/<int:pk>',views.block_vendor,name='block_vendor'),
    path('vendor_request/',views.admin_vendor_request_view, name='vendor_request'),
    path('vendor_request_accept/<int:pk>', views.admin_vendor_request_accept, name='vendor_request_accept'),

    path('view_product/',views.view_product, name='view_product'),
    path('edit_product/<str:slug>',views.edit_product, name='edit_product'),
    path('add_product/',views.addproduct, name='add_product'),

    path('pending_product_manage/<int:id>', views.admin_vendor_addproduct_accept, name='pending_product_manage'),

    path('view_vendor_pending_product/',views.view_vendor_pending_product,name='view_vendor_pending_product'),

    path('view_unlisted_product_admin/',views.view_unlisted_product_admin, name='view_unlisted_product_admin'),
    path('unlist_product_manage_admin/<int:id>',views.unlist_product_manage_admin, name='unlist_product_manage_admin'),

    path('add_maincategory/', views.add_maincategory, name='add_maincategory'),
    path('add_category/', views.add_category, name='add_category'),
    path('view_main_category/', views.view_main_category, name='view_main_category'),
    path('view_category/', views.view_category, name='view_category'),


    path('view_coupons/', views.view_coupons, name = 'view_coupons'),
    path('add_coupons/', views.add_coupons, name = 'add_coupons'),
]
