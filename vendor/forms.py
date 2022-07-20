from django import forms
from accounts . models import Account
from store . models import Product

class vendor_login_form(forms.ModelForm):
    password         = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    class Meta:
        model = Account
        fields = ['email','password']

    def __init__ (self, *args, **kwargs):
        super(vendor_login_form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "Enter your email"     
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        def clean(self):
            clean_data  = super(vendor_login_form, self).clean()
            email = clean_data.get('email')
            password = clean_data.get('password')
            vendor_side = Account.objects.filter(is_staff = True)
            if email not in vendor_side.email:
                raise forms.ValidationError('You are not an vendor')
            if password not in vendor_side.password:
                raise forms.ValidationError('Invalid password') 

class vendor_reg_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','GST_no','account_no','PAN_no','password',]

    def __init__ (self, *args,**kwargs):
        super(vendor_reg_form,self).__init__(*args,**kwargs)          
        self.fields['email'].widget.attrs['placeholder']='Enter your email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'      
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'  
        self.fields['GST_no'].widget.attrs['placeholder'] = 'Enter your GST no' 
        self.fields['account_no'].widget.attrs['placeholder'] = 'Enter your account no' 
        self.fields['PAN_no'].widget.attrs['placeholder'] = 'Enter your PAN no' 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        def clean(self):
            cleaned_data     = super(vendor_reg_form, self).clean()
            password         = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')
            if password != confirm_password:
                raise forms.ValidationError('Password does not match !')


                                                      
# class edit_product_form(forms.ModelForm):
    
#     class Meta:
#         model = Product
#         fields =[ 'images', 'product_name', 'category', 'stock', 'price', 'description', 'is_available']
        
#     def __init__ (self, *args, **kwargs):
#         super(edit_product_form, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'     
#             self.fields['is_available'].widget.attrs['class'] = ''
        

class add_product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'images', 'product_name', 'main_category', 'category', 'stock', 'mrp', 'price', 'description','is_available']
        widgets = {
            "images":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"images",
                "type":"file"
            })
        }
    def __init__ (self,*args,**kwargs):
        super(add_product_form,self).__init__(*args,**kwargs)
       
        self.fields['main_category'].widget.attrs['class'] = 'form-control'

        self.fields['category'].widget.attrs['class'] = 'form-control'

        self.fields['product_name'].widget.attrs['placeholder'] = 'product name'
        self.fields['product_name'].widget.attrs['class'] = 'form-control'
        self.fields['product_name'].widget.attrs['type'] = 'text'

        self.fields['stock'].widget.attrs['placeholder'] = 'available stock'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['type'] = 'text'
        
        self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_available'].widget.attrs['type'] = 'checkbox '

        self.fields['mrp'].widget.attrs['placeholder'] = 'mrp'
        self.fields['mrp'].widget.attrs['class'] = 'form-control'
        self.fields['mrp'].widget.attrs['type'] = 'text'

        self.fields['price'].widget.attrs['placeholder'] = 'price'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'product description'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = '3'
