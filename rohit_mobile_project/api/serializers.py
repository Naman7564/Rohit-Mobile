"""
API Serializers for Products and Inventory
"""
from rest_framework import serializers
from products.models import Product, Brand, Category, ProductImage
from inventory.models import InventoryTransaction, LowStockAlert


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'description']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']


class ProductListSerializer(serializers.ModelSerializer):
    """Minimal serializer for product lists"""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand_name', 'category', 'price', 
            'discount_price', 'image', 'stock_quantity', 'discount_percentage',
            'is_featured', 'created_at'
        ]
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for product details"""
    brand = BrandSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    additional_images = ProductImageSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'category', 'category_display', 
            'model_number', 'price', 'discount_price', 'description', 
            'image', 'stock_quantity', 'sku', 'color', 'storage_variant',
            'created_at', 'updated_at', 'is_active', 'is_featured',
            'additional_images', 'discount_percentage', 'is_low_stock'
        ]
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()
    
    def get_is_low_stock(self, obj):
        return obj.is_low_stock()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products"""
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    
    class Meta:
        model = Product
        fields = [
            'name', 'brand', 'category', 'model_number', 'price', 
            'discount_price', 'description', 'image', 'stock_quantity', 
            'sku', 'color', 'storage_variant', 'is_active', 'is_featured'
        ]
    
    def validate_sku(self, value):
        """Ensure SKU is unique"""
        instance = self.instance
        if instance:
            if Product.objects.filter(sku=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("SKU must be unique")
        else:
            if Product.objects.filter(sku=value).exists():
                raise serializers.ValidationError("SKU must be unique")
        return value


class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'product', 'product_name', 'transaction_type', 
            'quantity', 'notes', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LowStockAlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)
    product_stock = serializers.CharField(source='product.stock_quantity', read_only=True)
    
    class Meta:
        model = LowStockAlert
        fields = [
            'id', 'product', 'product_name', 'product_image', 'product_stock',
            'threshold', 'status', 'created_at', 'acknowledged_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'acknowledged_at', 'resolved_at']
