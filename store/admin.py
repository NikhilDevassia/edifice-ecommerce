from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'main_category', 'category', 'modified_date' ,'is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(Product, ProductAdmin)

admin.site.register(slider)
admin.site.register(MultipleImages)

admin.site.register(banner)

admin.site.register(ReviewRating)

admin.site.register(ProductRecommendation)
    
