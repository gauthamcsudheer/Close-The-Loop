# Generated by Django 5.0.7 on 2024-07-19 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
