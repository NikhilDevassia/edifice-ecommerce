from django.urls import reverse
from django.db import models
from category .models import Category, Main_category
from accounts .models import Account
from django.db.models import Avg,Count
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200, unique=True)
    description  = models.TextField(max_length=2500, blank=True)
    price        = models.IntegerField()
    mrp          = models.IntegerField()
    images       = models.ImageField(upload_to='media/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    main_category = models.ForeignKey(Main_category, on_delete=models.CASCADE,null=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    vendor       = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_permission = models.BooleanField(default=False)
    def __str__ (self):
        return self.product_name

    def offer(self):
        mrp,price = self.mrp,self.price 
        offer = int(((mrp-price)/mrp)*100)
        return offer

    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg 

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

#multiple image
class MultipleImages(models.Model):
    image = models.ImageField(upload_to='media/product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
# coding standartd
# slider category

class slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arraivels', 'New Arraivels')
    )

    Image         = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    SALE          = models.IntegerField()
    Brand_Name    = models.CharField(max_length=200)
    Discount      = models.IntegerField()
    Link          = models.CharField(max_length=200)

    def __str__(self):
        return self.Brand_Name	        


#banner category        
class banner(models.Model):
    image         = models.ImageField(upload_to='media/banner_imgs')
    discount_deal = models.CharField(max_length=100)
    quote         = models.CharField(max_length=100)
    discount      = models.IntegerField()

    def __str__(self):
        return self.quote



#review and rating
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


#product recommendation

class ProductRecommendation(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id    = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user_id.username