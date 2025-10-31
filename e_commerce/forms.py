from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from .models import Vendor, Product, Order, OrderItem
from .models import Customer, Vendor


#vendor registration
class VendorRegistrationForm(UserCreationForm):
    shop_name = forms.CharField(max_length=255)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'shop_name', 'bio']
        help_texts = {   # remove default help texts
            'username': None,
            'password1': None,
            'password2': None,
            'email': None,
            'shop_name': None,
            'bio': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        user.is_customer = False

        if commit:
            user.save()
            Vendor.objects.create(
                user=user,
                shop_name=self.cleaned_data['shop_name'],
                bio=self.cleaned_data['bio']
            )
        return user
    
#user registration
class CustomerRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {   # remove default help texts
            'username': None,
            'password1': None,
            'password2': None,
            'email': None,
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = False
        user.is_customer = True
        if commit:
            user.save()
        return user
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendor','name', 'description', 'price', 'stock', 'image']    
    

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    
    shipping_address_1 = forms.CharField(max_length=255, required=True)
    shipping_address_2 = forms.CharField(max_length=255, required=False)
    shipping_city = forms.CharField(max_length=100, required=True)
    shipping_state = forms.CharField(max_length=100, required=True)
    shipping_zip = forms.CharField(max_length=20, required=True)
    shipping_country = forms.CharField(max_length=100, required=True)
    cardholder_name = forms.CharField(max_length=100, required=True)
    delivery_instructions = forms.CharField(widget=forms.Textarea, required=False)
