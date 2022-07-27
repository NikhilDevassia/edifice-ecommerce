from cProfile import label
from hashlib import new
from django.shortcuts import redirect, render
from django.contrib import auth
from accounts.models import Account
from category.models import Main_category
from store.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.template.defaultfilters import slugify
from order.models import Order, OrderProduct
from django.db.models import Sum
#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth,TruncMinute,TruncDay
import datetime



#admin login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect(admin_home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_admin:
                auth.login(request, user)
                return redirect(admin_home)
            else:
                messages.error(request, 'You are not an admin !')  
                return redirect('admin_login')  
            # messages.error(request, 'Invalid email or password !')    
    form = admin_login_form()    
    context = {'form':form}             
    return render(request, 'adminpannel/admin_login.html',context)
    

#admin logout
@login_required(login_url= 'admin_login')
def admin_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('admin_login')         


#admin pannel
@login_required(login_url= 'admin_login')
def admin_home(request):
    orders_total = 0
    gross_sales = 0
    maincat_name = []
    maincat_sold = []
    chart_year = datetime.date.today().year
    chart_month = datetime.date.today().month
    orders_total = OrderProduct.objects.filter(product__vendor = request.user).count()
    sales = Product.objects.all().order_by('-count_sold')


    main_category = Main_category.objects.all()
    for main in main_category:
        maincat_name.append(main.category_name)
        maincat_sold.append(main.count_sold)

    orders_total = OrderProduct.objects.all().count()
    gross_sales = Order.objects.filter(is_ordered=True).aggregate(sum=Sum('order_total'))['sum'] 
    if gross_sales == None:
        gross_sales = 0
    profit = round(((int(gross_sales) * 0.15)))
    total = (gross_sales)    

    #getting daily revenue
    daily_revenue = Order.objects.filter(                     
    created_at__year=chart_year,created_at__month=chart_month
    ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_total')).values('day','sum')

    day=[]
    revenue=[]
    for i in daily_revenue:
        day.append(i['day'].minute)
        revenue.append(int(i['sum']))


    context = {
        'main_category':main_category,
        'sales':orders_total,
        'profit':profit,
        'total':total,
        'day':day,
        'revenue':revenue,
        'maincat_name':maincat_name,
        'maincat_sold':maincat_sold,
    }
    return render(request,'adminpannel/admin_home.html',context)

#user information
@login_required(login_url= 'admin_login')
def admin_user_manage(request):
    account = Account.objects.filter(is_admin=False,is_staff=False)
    context = {
        'users':account,
    }
    return render(request, 'adminpannel/userdetails.html',context)
        

#block user
@login_required(login_url= 'admin_login')
def block_user(request,pk):
    if request.method == 'POST':
        user = Account.objects.get(id=pk)
        user.is_active = False
        user.save()
        return redirect('admin_user')    

#unblock user
@login_required(login_url= 'admin_login')
def unblock_user(request,pk):
    if request.method == 'POST':
        user = Account.objects.get(id=pk)
        user.is_active = True
        user.save()
        return redirect('admin_user')         

#manage vendor
@login_required(login_url= 'admin_login')
def admin_vendor_manage(request):
    account = Account.objects.filter(is_admin=False,is_staff=True)
    context = {
        'vendors':account,
    }
    return render(request, 'adminpannel/vendor_details.html',context)


#vendor request accept
@login_required(login_url= 'admin_login')
def admin_vendor_request_view(request):
    account = Account.objects.filter(is_admin=False,is_staff=True,account_verification=False)
    context = {
        'vendors':account,
    }
    return render(request, 'adminpannel/vendorrequest.html',context)


#vendor account varification
@login_required(login_url= 'admin_login')
def admin_vendor_request_accept(request,pk):
    if request.method == 'POST':
        user = Account.objects.get(id=pk)
        user.account_verification = True
        user.save()
        return redirect('vendor_request') 


#block vendor request
@login_required(login_url= 'admin_login')
def block_vendor(request,pk):
    if request.method == 'POST':
        vendor = Account.objects.get(id=pk)
        vendor.is_active = False
        vendor.save()
        return redirect('admin_vendor_manage')   


#unblock vendor
@login_required(login_url= 'admin_login')
def unblock_vendor(request,pk):
    if request.method == 'POST':
        vendor = Account.objects.get(id=pk)
        vendor.is_active = True
        vendor.save()
        return redirect('admin_vendor_manage')  





#view product
@login_required(login_url= 'admin_login')
def view_product(request):
    product = Product.objects.filter(is_available=True,product_permission=True)
    context = {
        'product':product
    }
    return render(request,'adminpannel/viewproduct.html',context)
    
    
# update product 
@login_required(login_url= 'admin_login')
def edit_product(request,slug):   
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':                                  
        form = edit_product_form(request.POST, request.FILES, instance=product)            
        if form.is_valid():                               
            form.save()       

    
    form = edit_product_form(instance=product)  
    slug = product.slug

    context = {   
        
        'form' : form,   
        'slug' : slug 
        }   
    return render(request,'adminpannel/editproduct.html',context)          


#add product
@login_required(login_url= 'admin_login')
def addproduct(request):
    if request.method == 'POST':
        form = add_product_form(request.POST,request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            form.save()
            slug        = slugify(product_name)
            product = Product.objects.get(product_name= product_name)
            product.slug = slug    
            product.save()
    form = add_product_form()
    product = Product.objects.all()
    context = {
    'product':product,
    'form':form
    }
    return render(request, 'adminpannel/addproduct.html',context)

def view_vendor_pending_product(request,):
    product = Product.objects.all().filter(product_permission=False)
    context = {
    'product':product,
    }    
    return render(request,'adminpannel/pendingProduct.html', context)


#vendor product accept
@login_required(login_url= 'admin_login')
def admin_vendor_addproduct_accept(request,id):
    product = Product.objects.get(id=id)    
    vendor = product.vendor
    product.product_permission = True
    product.save()

    #confirmation 
    current_site = get_current_site(request)
    mail_subject = 'success............!.'
    message = render_to_string('adminpannel/ProductConfirm.html',{  
        'user': vendor,
        'domain': current_site,
    })
    to_email = vendor.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])  
    send_email.send()
    messages.success(request,'Congradulations admin accept your products...!')
    return redirect('view_vendor_pending_product')


#view unlisted products
@login_required(login_url= 'admin_login')
def view_unlisted_product_admin(request):
    product = Product.objects.filter(is_available = False)
    context = {
        'product':product,
    }
    return render(request,'adminpannel/viewunlistedproduct.html',context)

def unlist_product_manage_admin(request,id):
    product = Product.objects.get(id=id)
    if product.is_available == True:
        product.is_available = False
        product.save()
        return redirect('view_product')    
    else:
        product.is_available = False
        product.is_available = True
        product.save()
        return redirect('view_unlisted_product_admin')  


#add main category
@login_required(login_url= 'admin_login')
def add_maincategory(request):
    form = MainCategory_form(request.POST,request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            form.save()    
            slug = slugify(category_name)    
            main_category = Main_category.objects.get(category_name = category_name)
            main_category.slug = slug
            main_category.save()
    context={
        'form':form,
    }    
    return render(request,'adminpannel/mainCategory.html',context)        


#add category
@login_required(login_url= 'admin_login')
def add_category(request):
    form = Category_form(request.POST,request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            form.save()    
            slug = slugify(category_name)    
            category_name = Category_form.objects.get(category_name = category_name)
            category_name.slug = slug
            category_name.save()
    context={
        'form':form,
    }    
    return render(request,'adminpannel/Category.html',context)  


#view main category
@login_required(login_url= 'admin_login')
def view_main_category(request):
    main_category = Main_category.objects.all()
    context = {
        'main_category':main_category
    }
    return render(request,'adminpannel/ViewMainCategory.html',context)


#view category
@login_required(login_url= 'admin_login')
def view_category(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request,'adminpannel/ViewCategory.html',context)



#coupon
@login_required(login_url= 'admin_login')
def add_coupons(request):
    form = Add_coupons_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    context = {
        'form':form
    }
    return render(request, 'adminpannel/AddCoupon.html',context)

@login_required(login_url= 'admin_login')
def view_coupons(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons':coupons,
    }
    return render(request, 'adminpannel/ViewCoupons.html', context)


#ordered product
@login_required(login_url = 'admin_login')
def product_order(request):
    order_list = Order.objects.filter(is_ordered = True, status = 'New')
    context = {
        'order_list':order_list
    }
    return render(request,'adminpannel/orderlist.html', context)

#accepted orders
@login_required(login_url = 'admin_login')
def accepted_order(request):
    order_list = Order.objects.filter(is_ordered = True, status = 'Accepted')
    context = {
        'order_list':order_list
    }
    return render(request,'adminpannel/AcceptedOrders.html', context)

#order canceld
@login_required(login_url = 'admin_login')  
def canceld_product_order(request):
    order_list = Order.objects.filter(is_ordered = False)
    context = {
        'order_list':order_list,
    }
    return render(request,'adminpannel/Cancelled_order.html',context)

#sold product
@login_required(login_url = 'admin_login')
def soldproduct_list(request):
    order_list = OrderProduct.objects.filter(ordered=True, order__status = 'Completed')
    context = {
        'order_list':order_list,
    }
    return render(request,'adminpannel/soldproduct_list.html',context)

#order confirm
@login_required(login_url= 'admin_login')
def order_confirm(request,id):
    if request.method == 'POST':
        order_status = Order.objects.get(id=id)
        order_status.status = 'Accepted'
        order_status.save()
        return redirect('product_order_admin')   

#order confirm
@login_required(login_url= 'admin_login')
def order_completed(request,id):
    if request.method == 'POST':
        order_status = Order.objects.get(id=id)
        order_status.status = 'Completed'
        order_status.save()
        return redirect('accepted_order_admin')   


