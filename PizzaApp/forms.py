from django import forms
from .models import Pizza
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple(),  
        }

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    
    card_number = forms.CharField(
        max_length=19,  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'card-number',
            'placeholder': '#### #### #### ####',
            'inputmode': 'numeric'
        })
    )

    
    expiry_date = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YYYY'
        })
    )

    def clean_expiry_date(self):
        """ Validate and convert MM/YYYY format to a valid date. """
        expiry = self.cleaned_data['expiry_date']
        try:
            month, year = expiry.split('/')
            expiry_date = datetime.date(int(year), int(month), 1)  
        except ValueError:
            raise forms.ValidationError("Enter a valid expiry date in MM/YYYY format.")
        return expiry_date  

    
    cvv = forms.CharField(
        max_length=4,
        label="CVV",  
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
