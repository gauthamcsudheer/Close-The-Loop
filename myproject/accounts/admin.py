from django.contrib import admin
from .models import Product, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'company_name', 'location')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'company_name', 'location', 'user')
    search_fields = ('name', 'company_name', 'location')
    list_filter = ('company_name', 'location')
