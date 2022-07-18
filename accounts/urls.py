from unicodedata import name
from django.urls import URLPattern, path
from .import views

urlpatterns = [
    #user
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword'),
    path('resetpasswordpage/',views.resetpasswordpage, name='resetpasswordpage'),

    path('dashboard/',views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_details/<int:order_id>/', views.order_detail, name='order_details'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),

    
]