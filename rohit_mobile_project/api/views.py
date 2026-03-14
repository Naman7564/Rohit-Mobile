"""
API Views for Products, Inventory, and AI Detection
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
import json
import os
from datetime import datetime

from rohit_mobile_project.products.models import Product, Brand, Category
from rohit_mobile_project.inventory.models import InventoryTransaction, LowStockAlert
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    InventoryTransactionSerializer, LowStockAlertSerializer
)
from rohit_mobile_project.ai_services.detector import AIProductDetector


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product CRUD operations"""
    queryset = Product.objects.filter(is_active=True)
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        else:
            return ProductCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by brand
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand_id=brand)
        
        # Search by name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Featured products
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all categories"""
        categories = Category.objects.all()
        serializer = ProductListSerializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def brands(self, request):
        """Get all brands"""
        brands = Brand.objects.all()
        from api.serializers import BrandSerializer
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        products = self.get_queryset().filter(is_featured=True)[:8]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def low_stock(self, request, pk=None):
        """Check if product is low on stock"""
        product = self.get_object()
        return Response({
            'id': product.id,
            'name': product.name,
            'stock_quantity': product.stock_quantity,
            'is_low_stock': product.is_low_stock()
        })


class AIProductDetectionView(viewsets.ViewSet):
    """ViewSet for AI-based product detection"""
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=False, methods=['post'])
    def detect(self, request):
        """
        Detect product from image using AI
        
        Expects:
        - image: Image file from camera or upload
        
        Returns:
        - Detected product details as JSON
        """
        if 'image' not in request.FILES:
            return Response(
                {'error': 'Image file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        
        # Save image temporarily
        temp_path = f'/tmp/product_image_{datetime.now().timestamp()}.jpg'
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            
            # Detect product using AI
            detector = AIProductDetector()
            product_data = detector.detect_product_from_image(temp_path)
            
            if product_data is None:
                return Response(
                    {'error': 'Failed to detect product from image'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(product_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing image: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @action(detail=False, methods=['post'])
    def create_from_detection(self, request):
        """
        Create product from AI detection results
        
        Expects:
        - image: Product image file
        - name: Product name
        - brand_id: Brand ID (optional)
        - category: Product category
        - model_number: Model number (optional)
        - description: Product description
        - price: Product price
        - discount_price: Discount price (optional)
        - stock_quantity: Stock quantity
        - sku: Stock Keeping Unit
        - color: Color (optional)
        - storage_variant: Storage variant (optional)
        """
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Inventory Management"""
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    
    def get_queryset(self):
        queryset = InventoryTransaction.objects.all()
        
        # Filter by product
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def add_stock(self, request):
        """Add stock to a product"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        notes = request.data.get('notes', '')
        
        if not product_id or not quantity:
            return Response(
                {'error': 'product_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = get_object_or_404(Product, id=product_id)
        product.stock_quantity += int(quantity)
        product.save()
        
        # Create transaction record
        transaction = InventoryTransaction.objects.create(
            product=product,
            transaction_type='add',
            quantity=quantity,
            notes=notes,
            created_by=request.user.username if request.user.is_authenticated else 'system'
        )
        
        serializer = InventoryTransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def remove_stock(self, request):
        """Remove stock from a product"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        notes = request.data.get('notes', '')
        
        if not product_id or not quantity:
            return Response(
                {'error': 'product_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = get_object_or_404(Product, id=product_id)
        quantity = int(quantity)
        
        if product.stock_quantity < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock_quantity -= quantity
        product.save()
        
        # Create transaction record
        transaction = InventoryTransaction.objects.create(
            product=product,
            transaction_type='remove',
            quantity=quantity,
            notes=notes,
            created_by=request.user.username if request.user.is_authenticated else 'system'
        )
        
        serializer = InventoryTransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def low_stock_alerts(self, request):
        """Get all low stock alerts"""
        alerts = LowStockAlert.objects.filter(status='pending')
        serializer = LowStockAlertSerializer(alerts, many=True)
        return Response(serializer.data)
