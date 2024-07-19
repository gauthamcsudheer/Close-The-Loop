from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('log-in/', views.log_in, name='log_in'),
    path('log-out/', views.log_out, name='log_out'),
    path('main/', views.main_page, name='main'),
    path('products/', views.product_list, name='product_list'),
    path('checkout/', views.selected_products, name='selected_products'),
]
