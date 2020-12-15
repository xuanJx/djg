from django import forms
from django.forms import ModelForm
from .models import Customer, Order

# Create your forms here.

class RegisterForm(forms.Form):
    username = forms.CharField(
        label = 'username',
        max_length = 128,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username here'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email here'
        })
    )
    phone = forms.CharField(
        label='Phone',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number here'
        })
    )
    password1 = forms.CharField(
        label = 'password',
        max_length = 30,
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter your password here'
        })
    )
    password2 = forms.CharField(
        label='confirm password',
        max_length=30,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'phone'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'please input you name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'please input you phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'please input you email'
            }),
        }

class OrderForm(ModelForm):
    class Meta:
        model = Order
        filter = '__all__'
        exclude = ['time_created']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'please input you name'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'please input you phone number'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'please input you email'
            }),
        }