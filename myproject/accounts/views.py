from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProductForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Product

from geopy.geocoders import Nominatim
import itertools
from math import radians, sin, cos, sqrt, atan2

def home(request):
    return render(request, 'accounts/home.html')

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
        form = ProductForm(request.POST, request.FILES, user=request.user)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('main')  # Redirect to the same page or another page after saving
    else:
        form = ProductForm(user=request.user)
    return render(request, 'accounts/main.html', {'form': form})

def product_list(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, 'accounts/product_list.html', {'products': products})

@login_required
def selected_products(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('product_ids')
        products = Product.objects.filter(id__in=selected_ids)
        total_amount = sum(product.amount for product in products)
        
        return render(request, 'accounts/checkout.html', {
            'products': products,
            'total_amount': total_amount,
        })
    else:
        return redirect('product_list')
    

def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def total_distance(route):
    return sum(haversine_distance(route[i], route[i+1]) for i in range(len(route)-1)) + haversine_distance(route[-1], route[0])

def travelling_salesman(cities):
    shortest_route = None
    min_distance = float('inf')
    
    for perm in itertools.permutations(cities):
        current_distance = total_distance([city[1] for city in perm])
        if current_distance < min_distance:
            min_distance = current_distance
            shortest_route = perm
    
    return shortest_route, min_distance

def get_coordinates(city):
    geolocator = Nominatim(user_agent="tsp_solver")
    location = geolocator.geocode(city)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"Coordinates for city {city} not found")

def shortest_path_view(request):
    # Assuming 'Product' model has a 'location' field which stores the city names
    locations = Product.objects.values_list('location', flat=True).distinct()
    cities_coords = [(city, get_coordinates(city)) for city in locations]

    route, distance = travelling_salesman(cities_coords)
    route_with_names = [city[0] for city in route]

    context = {
        'route': route_with_names,
        'distance': distance,
    }

    return render(request, 'accounts/shortest_path.html', context)