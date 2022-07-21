from django.shortcuts import render,redirect
from .forms import *
from accounts .models import Account
from django.contrib import messages,auth
from store .models import Product,MultipleImages
from django.template.defaultfilters import slugify
from order.models import Order,OrderProduct, Payment
#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

#vendor login
def vendor_login(request):
    if request.user.is_authenticated and request.user.is_staff and request.user.is_admin == False:
        return redirect('vendor_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('vendor_home')
            else:
                messages.error(request, 'You are not an vendor !')  
                return redirect('vendor_login')   
    form = vendor_login_form()    
    context = {'form':form}             
    return render(request, 'vendor/vendorlogin.html',context)


@login_required(login_url = 'vendor_login')
def vendor_home(request):
    profit = 0
    total_price = 0
    total = 0
    sales = 0
    total_price = OrderProduct.objects.filter(product__vendor = request.user).aggregate(Sum('product_price'))
    total = (total_price["product_price__sum"])
    profit = (total * 0.9)
    context = {
        'sales':sales,
        'profit':profit,
        'total':total,
    }
    return render(request,'vendor/vendorhome.html', context)       


#vendor logout
@login_required(login_url= 'vendor_login')
def vendor_logout(request):
    auth.logout(request)
    return redirect('vendor_login')  


#vendor register
def vendor_register(request):
    if request.method == 'POST':
            form = vendor_reg_form(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                GST_no = form.cleaned_data['GST_no']
                account_no = form.cleaned_data['account_no']
                PAN_no = form.cleaned_data['PAN_no']
                password = form.cleaned_data['password']
                username = email.split("@")[0]
    
                user = Account.objects.create_user(
                    first_name = first_name,
                    last_name  = last_name,
                    email      = email,
                    username   = username,
                    password   = password,
                )
                user.GST_no = GST_no
                user.PAN_no = PAN_no
                user.account_no = account_no
                user.save()

                #vendor activation mail
                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('vendor/vendor_activation.html',{
                    'user': user,
                    'domain': current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])  
                send_email.send()
                messages.success(request,'Registration Successful')
                return redirect('vendor_register')
    else:
        form = vendor_reg_form()
    context = {
        'form':form
    }
    return render(request,'vendor/vendorregister.html',context)


#vendor activation
def activate(request,uidb64,token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Congradulations  Your account is activated')
        return redirect('vendor_login')        
    else:
        messages.error(request,'Invalid activation link !')    
        return redirect(vendor_register)


#vendor reset password
def vendor_forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #forgot password 
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('vendor/vendor_reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])  
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('vendor_login')
        else:
            messages.error(request,' Account does not exist! ', extra_tags='reset')
            return render(request, 'vendor/forgotpassword.html')
    return render(request, 'vendor/forgotpassword.html')


#vendor reset password validation
def vendor_resetpassword_validate(request,uidb64,token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('vendor_resetpasswordpage')
    else:
        messages.error(request, 'This link is has been expired !')
        return redirect('vendor_login')


#vendor resetpassword
def vendor_resetpasswordpage(request):
    if request.method == 'POST':
        password        = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('vendor_login')
        else:
            messages.error(request, 'Password do not match !')    
            return redirect('vendor_resetpasswordpage')
    else:        
        return render(request, 'vendor/resetpassword.html') 


#Vendor view product
@login_required(login_url = 'vendor_login')
def viewproduct(request,id):
    product = Product.objects.filter(vendor=id,is_available=True,product_permission=True)
    context = {
        'product':product
    }
    return render(request,'vendor/viewproduct.html',context)     


#Edit product
@login_required(login_url = 'vendor_login')
def editproduct(request,slug):  
    product = Product.objects.get(slug=slug)

    if request.method == 'POST':     
        if len(request.FILES) != 0:
            images = image.objects.get(product=product)
            for image in images:
                image.delete()
            images = request.FILES.getlist('images')  
            for image in images:
                MultipleImages.objects.create(
                    image=image,
                    product = product,                   
                )  
        form = add_product_form(request.POST, request.FILES, instance=product)     
        if form.is_valid():                               
            form.save()      
           
    form = add_product_form(instance=product)  
    slug = product.slug
    context = {  
        'form' : form,   
        'slug' : slug 
        }   
    return render(request,'vendor/addproduct.html',context)       


#Add product
@login_required(login_url = 'vendor_login')
def add_product(request):
    if request.method == 'POST':
        form = add_product_form(request.POST,request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            category     = form.cleaned_data['category']
            stock        = form.cleaned_data['stock']
            mrp          = form.cleaned_data['mrp']
            price        = form.cleaned_data['price']
            description  = form.cleaned_data['description']
            images       = form.cleaned_data['images']
            is_available = form.cleaned_data['is_available']
            vendor       = request.user
            slug         = slugify(product_name)

            product = Product.objects.create(
                vendor       = vendor,
                product_name = product_name,
                slug         = slug,
                is_available = is_available,
                category     = category,
                stock        = stock,
                price        = price,
                mrp          = mrp,
                description  = description,
                images       = images,
                )   
            
            images = request.FILES.getlist('multiple_images')
            for image in images:
                MultipleImages.objects.create(
                    image=image,
                    product = product, #add images using for loop in list
                )

            #add product confirmation
            current_site = get_current_site(request)
            mail_subject = 'success.!.'
            message = render_to_string('vendor/confirmation.html',{
                'user': vendor,
                'domain': current_site,
            })
            to_email = vendor.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])  
            send_email.send()
            messages.success(request,'Successful')


            #send main to admin
            admin_mail = Account.objects.get(is_email = True)
            current_site = get_current_site(request)
            mail_subject = 'New product added'
            message = render_to_string('vendor/add_product_adminmail.html',{
                'user': vendor,
                'domain': current_site,
            })
            to_email = admin_mail.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])  
            send_email.send()

            
    else:
        form = add_product_form
    context={
        'form':form,
    }    
    return render(request, 'vendor/addproduct.html',context)


#view unlisted product
@login_required(login_url = 'vendor_login')
def view_unlisted_product(request,id):
    product = Product.objects.filter(vendor=id,is_available=False) 
    context = {
        'product':product
    }   
    return render(request,'vendor/unlisted.html',context)     


#unlist, list product
@login_required(login_url = 'vendor_login')
def unlist_product(request,id):
    product = Product.objects.get(id=id)
    if product.is_available == True:
        product.is_available = False
        product.save()
        return redirect('viewproduct',id=request.user.id)    
    else:
        product.is_available = False
        product.is_available = True
        product.save()
        return redirect('view_unlisted_product',id=request.user.id)    

# def product_order(request):
#     order_list = Order.objects.all()
#     context = {
#         'order_list':order_list
#     }
#     return render(request,'vendor/orderlist.html', context)


#ordered product
@login_required(login_url = 'vendor_login')
def product_order(request):
    order_list = Order.objects.all()
    context = {
        'order_list':order_list
    }
    return render(request,'vendor/orderlist.html', context)

#sold product
@login_required(login_url = 'vendor_login')
def soldproduct_list(request):
    soldproduct = Payment.objects.all()
    context = {
        'soldproduct':soldproduct,
    }
    return render(request,'vendor/soldproduct_list.html',context)




