from traceback import print_tb
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from . models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from coupon .models import Coupon,CouponUsers
# Create your views here.

def _cart_id(request): #private function
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart   



def add_cart(request, product_id):  
    current_user = request.user
    product = Product.objects.get(id=product_id) #get product id
    #if user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:  
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()    
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )    
            cart_item.save()
        return redirect('cart')
    else:   
        #if user is not authenticated 
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))  
        cart.save()   

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:  
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()    
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )    
            cart_item.save()

        return redirect('cart')




def remove_cart(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated: 
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')        



def remove_cart_item(request, product_id, cart_item_id): 
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:   
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



 
def cart(request, total=0, quantity=0, coupon=0, cart_items=None):  
    try:
        delivery_charge = 0
        grand_total = 0
        if request.user.is_authenticated:   
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            if CouponUsers.objects.filter(user=request.user, is_used=False).exists():
                coupon_user =  CouponUsers.objects.get(user=request.user, is_used=False)
                coupon = coupon_user.amount
            
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)          
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        delivery_charge = 1500  if  total<50000 else 0    
        grand_total = total + delivery_charge
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items, 
        'grand_total':grand_total - coupon if grand_total >= 50000 else grand_total,
        'delivery_charge':delivery_charge,
        'coupon':coupon,
    }        
    return render(request,'cart/cart.html',context)



def add_coupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        if Coupon.objects.filter(coupon_code=code, is_available=True).exists() and CouponUsers.objects.filter(user=request.user, coupon__coupon_code=code).exists()  == False:
            coupon_object = Coupon.objects.get(coupon_code=code, is_available=True)
            coupon_user = CouponUsers()
            coupon_user.user = request.user
            coupon_user.coupon = coupon_object
            coupon_user.is_used = True
            coupon_user.amount = coupon_object.amount
            coupon_user.save()

            coupon_object.quantity -= 1
            if coupon_object.quantity == 0:
                coupon_object.is_available = False
            coupon_object.save()
        return redirect('cart')





@login_required(login_url='login')
def checkout(request, total=0, quantity=0, coupon=0, cart_items=None):         
    try:
        delivery_charge = 0
        grand_total = 0
        if request.user.is_authenticated:   
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
       
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        if CouponUsers.objects.filter(user = request.user, is_used = False).exists():
            coupon_user = CouponUsers.objects.get(user=request.user, is_used=False)
            coupon = coupon_user.amount if total >= 50000 else 0

        delivery_charge = 1500  if  total >= 50000 else 0    
        grand_total = total + delivery_charge

    except ObjectDoesNotExist:
        pass

    context = { 
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items, 
        'grand_total':grand_total - coupon if grand_total >= 50000 else grand_total,
        'delivery_charge':delivery_charge,
        'coupon':coupon,
    }        
    print(grand_total)
    return render(request,'cart/checkout.html',context)

    
    

def coupon_page(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon
    }
    return render(request, 'cart/CouponPage.html',context)