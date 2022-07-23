from django.db.models import Count
from django.shortcuts import render
from store.models import slider,Product,ProductRecommendation
from category.models import Main_category
from accounts.models import Account
from order.models import OrderProduct
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        product_recommendation = ProductRecommendation.objects.filter(user_id=request.user).order_by('-created_at')
        is_rec_av = product_recommendation.exists()
        slid    = slider.objects.all()
        product = Product.objects.all().order_by('-created_date')[:10]
        top_selling = OrderProduct.objects.all().order_by('-quantity')
        main_category = Main_category.objects.all().order_by('-id') 

        context = { 
        'sliders':slid,
        'products':product,
        'main_category':main_category,
        'recommendations':product_recommendation,
        'is_rec_av':is_rec_av,
        'top_selling':top_selling,
        }   
        return render(request,'main/home.html', context)
    else:
        slid    = slider.objects.all()
        product = Product.objects.all().order_by('-created_date')[:10]
        top_selling = OrderProduct.objects.all().order_by('-quantity')
        main_category = Main_category.objects.all().order_by('-id')

        context = {
        'sliders':slid,
        'products':product,
        'main_category':main_category,
        'top_selling':top_selling,
        }   
        return render(request,'main/home.html', context)
def Error404(request):
    return render(request,'404.html')


