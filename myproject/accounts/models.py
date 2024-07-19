from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255, default='')

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Field for amount
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to CustomUser
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # New field for image

    def __str__(self):
        return self.name