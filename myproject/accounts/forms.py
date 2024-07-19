from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Product

class SignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Company Name',
        'class': 'input-field'
    }))
    location = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Location',
        'class': 'input-field'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'input-field'
    }))
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'input-field'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'input-field'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'input-field'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'company_name', 'location', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'input-field'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'input-field'
    }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'input-field'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'input-field'
        })

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'amount', 'image']  # Add 'image' field

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        if commit:
            instance.company_name = self.user.company_name
            instance.location = self.user.location
            instance.user = self.user
            instance.save()
        return instance