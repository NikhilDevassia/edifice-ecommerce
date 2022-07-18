from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def add_to_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        wishlist = WishList.objects.get(wishlist_id=_wishlist_id(request))
    except WishList.DoesNotExist:
        wishlist = WishList.objects.create(wishlist_id=_wishlist_id(request))
    wishlist.save()
    try:
        wishlist_item = WishListItem.objects.get(product=product, wishlist=wishlist)
        wishlist_item.save()
    except WishListItem.DoesNotExist:
        wishlist_item = WishListItem.objects.create(
            product = product,
            wishlist = wishlist,
        )  
        wishlist_item.save()
    return redirect(user_wishlist)  


def remove_wishlist_item(request,product_id):
    wishlist = WishList.objects.get(wishlist_id=_wishlist_id(request))
    product = get_object_or_404(Product, id=product_id)
    wihlist_item = WishListItem.objects.get(product=product, wishlist=wishlist)
    wihlist_item.delete()
    return redirect(user_wishlist)


def user_wishlist(request, wishlist_item = None):
    try:
        wishlist = WishList.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_item = WishListItem.objects.filter(wishlist=wishlist, is_active=True)
    except ObjectDoesNotExist:
        pass
    context = {
        'wishlist_item':wishlist_item,
    }
    return render(request,'wishlist/wishlist.html',context)