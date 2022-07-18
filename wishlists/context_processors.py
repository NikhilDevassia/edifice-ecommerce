from . models import WishList,WishListItem
from . views import _wishlist_id
 
def counter(request):
    wishlist_count = 0
    if 'admin' in request.path:
        return {}
 
    try:
        wishlist = WishList.objects.filter(wishlist_id = _wishlist_id(request))
        if request.user.is_authenticated:
            wishlist_items = WishListItem.objects.all().filter(user=request.user) 
        else:
            wishlist_items = WishListItem.objects.all().filter(wishlist=wishlist[:1])
        for wishlist_item in wishlist_items:
            wishlist_count += wishlist_item.quantity
            
    except WishList.DoesNotExist:
        wishlist_count = 5

    return dict(wishlist_count = wishlist_count)        