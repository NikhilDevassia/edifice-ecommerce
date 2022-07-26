from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='shop'),
    path('category/<slug:category_slug>/', views.store, name='category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
    path('search/', views.search, name='search'),
    path('submit_review/<slug:product_id>/', views.submit_review, name='submit_review'),
]

