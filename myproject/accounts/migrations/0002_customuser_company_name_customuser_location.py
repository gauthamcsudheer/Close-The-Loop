# Generated by Django 5.0.7 on 2024-07-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.CharField(default='', max_length=255),
        ),
    ]