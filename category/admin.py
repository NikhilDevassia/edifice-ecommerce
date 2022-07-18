from django.contrib import admin
from .models import Category, Main_category, Sub_category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug', 'main_category')
admin.site.register(Category, CategoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug', 'category')
admin.site.register(Sub_category, CategoryAdmin)
 
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug')
admin.site.register(Main_category, CategoryAdmin)