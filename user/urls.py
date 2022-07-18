from django.urls import path
from . import views

urlpatterns = [
    path('404/',views.Error404,name='404'),
    path('',views.home, name='home'),
]