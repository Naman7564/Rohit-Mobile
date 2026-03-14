"""
Django Admin Configuration for Products and Inventory
"""
from django.contrib import admin
from .models import Product, Brand, Category, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'brand', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'model_number', 'sku']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'brand', 'category', 'model_number', 'sku'),
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price'),
        }),
        ('Details', {
            'fields': ('description', 'image', 'color', 'storage_variant'),
        }),
        ('Stock Management', {
            'fields': ('stock_quantity',),
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_featured', 'unmark_featured']
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_featured.short_description = "Mark selected products as featured"
    
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
    unmark_featured.short_description = "Unmark selected products as featured"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'alt_text']
