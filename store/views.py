from django.shortcuts import get_object_or_404, redirect, render
from cartapp.models import CartItem
import user
from .models import *
from category.models import Category,Main_category
from django.db.models import Max,Min
from cartapp .models import CartItem
from cartapp.views import _cart_id
from django.db.models import Q
from . forms import ReviewForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from order.models import Order, OrderProduct
# Create your views here.


def store(request, category_slug=None):
    main_category = Main_category.objects.all().order_by('-id')
    if category_slug != None: 
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories, is_available=True, product_permission=True)
        paginators = Paginator(products, 8)
        page = request.GET.get('page')
        paged_product = paginators.get_page(page)
       
    else:
        products = Product.objects.all().filter(is_available=True, product_permission=True).order_by('id')
        paginators = Paginator(products, 8)
        page = request.GET.get('page')
        paged_product = paginators.get_page(page)
        # product_count = product.count()

    FilterPrice = request.GET.get('FilterPrice')
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        products = Product.objects.filter(price__lte = Int_FilterPrice)
    categories = Category.objects.all()    
    
    context = {
        'main_category':main_category,
        'min_price':min_price,
        'max_price':max_price, 
        'products':paged_product,
        'categories':categories,
        'FilterPrice':FilterPrice,
    }    

    return render(request, 'store/store.html',context)  


def product_details(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        multiple_images = MultipleImages.objects.filter(product=single_product)
        if request.user.is_authenticated:
             in_cart = CartItem.objects.filter(user=request.user,product = single_product).exists()
        else:
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product).exists()
        # in_cart_login = CartItem.objects.filter(user=request.user,product = single_product).exists()

    except Exception as e:
        return e    

    if request.user.is_authenticated:
    
        if ProductRecommendation.objects.filter(product_id=single_product, user_id=request.user).exists():
            pass
        else:
            product_recommendation = ProductRecommendation.objects.create(
                product_id = single_product,
                user_id    = request.user

            )
            product_recommendation.save()
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        #Get the review
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)


    context = {
        'multiple_images':multiple_images,
        'single_product':single_product ,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
    } 
    return render(request,'store/product_details.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(price__icontains=keyword) | Q(description__icontains=keyword) ) 
            product_count = products.count()
    context = {
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context) 


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


