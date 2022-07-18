from django.urls import reverse
from django.db import models


# Main category
class Main_category(models.Model):
    category_name = models.CharField(max_length=100)
    slug          = models.SlugField(max_length=100, unique=True, null=True)
    description   = models.TextField(max_length=2000, null=True)
    cat_image     = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name = 'main_category'
        verbose_name_plural = 'main_categories'

    def __str__(self):
        return self.category_name

#category
class Category(models.Model):
    main_category = models.ForeignKey(Main_category, on_delete=models.CASCADE, null=True)
    category_name = models.CharField(max_length=50)
    slug          = models.SlugField(max_length=100, unique=True, null=True)
    description   = models.TextField(max_length=2000,null=True)
    cat_image     = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('category', args=[self.slug])

    def __str__ (self):
        return self.category_name
        # return self.category_name + "---" + self.main_category.category_name

#Sub category
class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    category_name = models.CharField(max_length=50)
    slug          = models.SlugField(max_length=100, unique=True, null=True)
    description   = models.TextField(max_length=2000,null=True)
    cat_image     = models.ImageField(upload_to='media/categories',blank=True)

    class Meta:
        verbose_name = 'sub_category'
        verbose_name_plural = 'sub_categories'

    def __str__(self):
        return self.category.main_category.category_name + " " + self.category.category_name + " " + self.category_name
# Create your models here.
