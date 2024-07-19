from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProductForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Product

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('main')  # Redirect to 'main' or another page
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main')  # Redirect to 'main' or another page
    else:
        form = LoginForm()
    return render(request, 'accounts/log_in.html', {'form': form})

def log_out(request):
    auth_logout(request)
    return redirect('main')  # Redirect to 'main' or another page

@login_required
def main_page(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('main')  # Redirect to the same page or another page after saving
    else:
        form = ProductForm(user=request.user)
    return render(request, 'accounts/main.html', {'form': form})

def product_list(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, 'accounts/product_list.html', {'products': products})

def selected_products(request):
    # Get selected product IDs from the POST request
    selected_ids = request.POST.getlist('product_ids')
    
    # Fetch the selected products from the database
    products = Product.objects.filter(id__in=selected_ids)
    
    # Calculate the total amount
    total_amount = sum(product.amount for product in products)
    
    return render(request, 'accounts/selected_products.html', {
        'products': products,
        'total_amount': total_amount
    })