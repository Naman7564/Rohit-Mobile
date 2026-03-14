from django.db import models
from django.utils import timezone

class Category(models.Model):
    """Product Category Model"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon class name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    """Product Brand Model"""
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model"""
    CATEGORY_CHOICES = [
        ('mobile', 'Mobile Phone'),
        ('charger', 'Charger'),
        ('cable', 'Cable'),
        ('earbuds', 'Earbuds'),
        ('accessories', 'Accessories'),
    ]
    
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    model_number = models.CharField(max_length=100, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    
    color = models.CharField(max_length=50, blank=True)
    storage_variant = models.CharField(max_length=100, blank=True)  # e.g., "128GB", "256GB"
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_discount_percentage(self):
        if self.discount_price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount, 2)
        return 0
    
    def is_low_stock(self, threshold=10):
        return self.stock_quantity < threshold


class ProductImage(models.Model):
    """Additional Product Images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/additional/')
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Image for {self.product.name}"
