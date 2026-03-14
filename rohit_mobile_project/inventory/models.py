from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product
from django.utils import timezone

class InventoryTransaction(models.Model):
    """Track inventory changes"""
    TRANSACTION_TYPE_CHOICES = [
        ('add', 'Add Stock'),
        ('remove', 'Remove Stock'),
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('damage', 'Damaged'),
        ('adjustment', 'Stock Adjustment'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"


class LowStockAlert(models.Model):
    """Track low stock alerts"""
    ALERT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='low_stock_alerts')
    threshold = models.IntegerField(default=10)
    status = models.CharField(max_length=20, choices=ALERT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Low Stock Alert - {self.product.name}"
    
    def acknowledge(self):
        self.status = 'acknowledged'
        self.acknowledged_at = timezone.now()
        self.save()
    
    def resolve(self):
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()
