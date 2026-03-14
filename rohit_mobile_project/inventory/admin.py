"""
Django Admin Configuration for Inventory
"""
from django.contrib import admin
from .models import InventoryTransaction, LowStockAlert


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'created_at', 'created_by']
    list_filter = ['transaction_type', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['product__name', 'notes']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('product', 'transaction_type'),
        }),
        ('Transaction Details', {
            'fields': ('quantity', 'notes'),
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(LowStockAlert)
class LowStockAlertAdmin(admin.ModelAdmin):
    list_display = ['product', 'threshold', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'acknowledged_at', 'resolved_at']
    search_fields = ['product__name']
    
    actions = ['acknowledge_alerts', 'resolve_alerts']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('product', 'threshold', 'status'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'acknowledged_at', 'resolved_at'),
        }),
    )
    
    def acknowledge_alerts(self, request, queryset):
        for alert in queryset:
            alert.acknowledge()
    acknowledge_alerts.short_description = "Acknowledge selected alerts"
    
    def resolve_alerts(self, request, queryset):
        for alert in queryset:
            alert.resolve()
    resolve_alerts.short_description = "Resolve selected alerts"
