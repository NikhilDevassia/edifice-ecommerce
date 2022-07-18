from django.db import models
from store . models import Product
from accounts . models import Account
# Create your models here.

class WishList(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    added_date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id

class WishListItem(models.Model):
    user     = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product   = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist  = models.ForeignKey(WishList,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)        

    def __str__(self):
        return self.product.product_name