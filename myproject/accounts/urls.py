from django.urls import path
from .views import sign_up, log_in, log_out, main_page, product_list, selected_products

urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('log-in/', log_in, name='log_in'),
    path('log-out/', log_out, name='log_out'),
    path('main/', main_page, name='main'),
    path('products/', product_list, name='product_list'),
     path('selected-products/', selected_products, name='selected_products'),
]
