from dataclasses import field
from django import forms
from . models import *
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','review', 'rating']