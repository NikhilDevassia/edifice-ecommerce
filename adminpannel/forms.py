from django import forms
from coupon.models import Coupon
from store.models import Product
from accounts.models import Account
from category.models import Main_category,Category



class admin_login_form(forms.ModelForm):
    password         = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    class Meta:
        model = Account
        fields = ['email','password']

    def __init__ (self, *args, **kwargs):
        super(admin_login_form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "Enter your email"     
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        def clean(self):
            clean_data  = super(admin_login_form, self).clean()
            email = clean_data.get('email')
            password = clean_data.get('password')
            admin_side = Account.objects.filter(is_admin = True)
            if email not in admin_side.email:
                raise forms.ValidationError('You are not an admin')
            if password not in admin_side.password:
                raise forms.ValidationError('Invalid password')    
        

class edit_product_form(forms.ModelForm):
    
    class Meta:
        model = Product
        fields =[ 'images', 'product_name', 'category', 'stock', 'mrp', 'price', 'description', 'is_available']
        
    def __init__ (self, *args, **kwargs):
        super(edit_product_form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'     
            self.fields['is_available'].widget.attrs['class'] = ''
        

class add_product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'images', 'product_name', 'category', 'stock', 'mrp', 'price', 'description']
    def __init__ (self,*args,**kwargs):
        super(add_product_form,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
          



class MainCategory_form(forms.ModelForm):
    class Meta:
        model = Main_category
        fields = ['cat_image', 'category_name','description']
        widgets = {
            "primary_image":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"primary_image",
                "type":"file"
            })
        }   
    def __init__ (self, *args, **kwargs):
        super(MainCategory_form, self).__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs['placeholder'] = 'Enter main category name'
        self.fields['category_name'].widget.attrs['class'] = 'form-control'
        self.fields['category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'product description'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = '3'




class Category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cat_image', 'category_name','description']
        widgets = {
            "primary_image":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"primary_image",
                "type":"file"
            })  
        }   
    def __init__ (self, *args, **kwargs):
        super(Category_form, self).__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs['placeholder'] = 'Enter category name'
        self.fields['category_name'].widget.attrs['class'] = 'form-control'
        self.fields['category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'product description'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = '3'








class Add_coupons_form(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'amount','quantity', 'is_available']
        widgets = {
            "primary_image":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"primary_image",
                "type":"file"
            })  
        }   
    def __init__ (self, *args, **kwargs):
        super(Add_coupons_form, self).__init__(*args, **kwargs)
        self.fields['coupon_code'].widget.attrs['placeholder'] = 'Enter coupon code '
        self.fields['coupon_code'].widget.attrs['class'] = 'form-control'
        self.fields['coupon_code'].widget.attrs['type'] = 'text'

        self.fields['amount'].widget.attrs['placeholder'] = 'mrp'
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['amount'].widget.attrs['type'] = 'text'

        self.fields['quantity'].widget.attrs['placeholder'] = 'mrp'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['type'] = 'text'

