from django import forms
from . models import Account,UserProfile

class RegistrationForm(forms.ModelForm):
    first_name       = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Password'}))
    last_name        = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Password'}))
    email            = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Enter Password'}))
    password         = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    
    class Meta:

        model  = Account
        fields = ['first_name','last_name','email','password'] 


    def clean(self):
        cleaned_data     = super(RegistrationForm, self).clean()
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match !')


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'