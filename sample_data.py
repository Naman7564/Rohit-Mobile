"""
Sample data population script for Rohit Mobile
Run with: python manage.py shell < sample_data.py
"""

from products.models import Product, Brand, Category
from decimal import Decimal
import os

print("Creating sample data...")

# Create categories
print("Creating categories...")
categories_data = [
    {'name': 'Mobile Phone', 'slug': 'mobile', 'icon': '📱'},
    {'name': 'Charger', 'slug': 'charger', 'icon': '🔌'},
    {'name': 'Cable', 'slug': 'cable', 'icon': '🔗'},
    {'name': 'Earbuds', 'slug': 'earbuds', 'icon': '🎧'},
    {'name': 'Accessories', 'slug': 'accessories', 'icon': '💎'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'icon': cat_data['icon']
        }
    )
    categories[cat_data['slug']] = cat
    print(f"  {'Created' if created else 'Exists'}: {cat.name}")

# Create brands
print("\nCreating brands...")
brands_data = ['Samsung', 'Apple', 'OnePlus', 'Xiaomi', 'Google', 'Realme', 'Oppo', 'Vivo']
brands = {}
for brand_name in brands_data:
    brand, created = Brand.objects.get_or_create(
        name=brand_name,
        defaults={'description': f'{brand_name} products'}
    )
    brands[brand_name] = brand
    print(f"  {'Created' if created else 'Exists'}: {brand.name}")

# Create sample products
print("\nCreating sample products...")
products_data = [
    {
        'name': 'Samsung Galaxy S23 Ultra',
        'brand': 'Samsung',
        'category': 'mobile',
        'model_number': 'SM-S918B',
        'price': Decimal('124999'),
        'discount_price': Decimal('99999'),
        'description': 'Premium flagship with 200MP camera and 120Hz display',
        'stock_quantity': 15,
        'sku': 'SGS23ULTRA001',
        'color': 'Phantom Black',
        'storage_variant': '256GB',
        'is_featured': True,
    },
    {
        'name': 'iPhone 15 Pro Max',
        'brand': 'Apple',
        'category': 'mobile',
        'model_number': 'A2846',
        'price': Decimal('139999'),
        'discount_price': Decimal('129999'),
        'description': 'Latest Apple flagship with A17 Pro chip',
        'stock_quantity': 8,
        'sku': 'IPH15PRO001',
        'color': 'Deep Purple',
        'storage_variant': '256GB',
        'is_featured': True,
    },
    {
        'name': 'OnePlus 11 Pro',
        'brand': 'OnePlus',
        'category': 'mobile',
        'model_number': 'CPH2307',
        'price': Decimal('89999'),
        'discount_price': Decimal('75999'),
        'description': 'Fast Android device with 120Hz AMOLED display',
        'stock_quantity': 20,
        'sku': 'OP11PRO001',
        'color': 'Eternal Green',
        'storage_variant': '128GB',
        'is_featured': True,
    },
    {
        'name': 'Samsung Super Fast Charger',
        'brand': 'Samsung',
        'category': 'charger',
        'model_number': 'EP-TA20',
        'price': Decimal('2999'),
        'discount_price': Decimal('1999'),
        'description': '25W super fast charging for all Samsung devices',
        'stock_quantity': 50,
        'sku': 'SAMCHARGE001',
        'color': 'White',
        'storage_variant': '',
        'is_featured': False,
    },
    {
        'name': 'USB-C Cable 3m',
        'brand': 'OnePlus',
        'category': 'cable',
        'model_number': 'C1008',
        'price': Decimal('499'),
        'discount_price': Decimal('299'),
        'description': 'High-speed USB-C charging and data cable',
        'stock_quantity': 100,
        'sku': 'OPCABLE001',
        'color': 'Black',
        'storage_variant': '',
        'is_featured': False,
    },
    {
        'name': 'Samsung Galaxy Buds2 Pro',
        'brand': 'Samsung',
        'category': 'earbuds',
        'model_number': 'SM-R510',
        'price': Decimal('14999'),
        'discount_price': Decimal('9999'),
        'description': 'Premium wireless earbuds with ANC',
        'stock_quantity': 25,
        'sku': 'SAMBUDS001',
        'color': 'Black',
        'storage_variant': '',
        'is_featured': True,
    },
    {
        'name': 'Phone Screen Protector',
        'brand': 'Realme',
        'category': 'accessories',
        'model_number': 'SP-001',
        'price': Decimal('299'),
        'discount_price': Decimal('199'),
        'description': 'Tempered glass screen protector for all phones',
        'stock_quantity': 200,
        'sku': 'REALSCR001',
        'color': 'Clear',
        'storage_variant': '',
        'is_featured': False,
    },
    {
        'name': 'Phone Case Premium Leather',
        'brand': 'Generic',
        'category': 'accessories',
        'model_number': 'CASE-001',
        'price': Decimal('699'),
        'discount_price': Decimal('499'),
        'description': 'Premium leather phone case with card slots',
        'stock_quantity': 75,
        'sku': 'CASE001',
        'color': 'Brown',
        'storage_variant': '',
        'is_featured': False,
    },
    {
        'name': 'Xiaomi Redmi Note 12',
        'brand': 'Xiaomi',
        'category': 'mobile',
        'model_number': '23041216U',
        'price': Decimal('24999'),
        'discount_price': Decimal('19999'),
        'description': 'Budget-friendly with great performance',
        'stock_quantity': 30,
        'sku': 'XMIRDN12001',
        'color': 'Midnight Black',
        'storage_variant': '128GB',
        'is_featured': False,
    },
    {
        'name': 'Google Pixel 7 Pro',
        'brand': 'Google',
        'category': 'mobile',
        'model_number': 'GR1YH',
        'price': Decimal('84999'),
        'discount_price': Decimal('69999'),
        'description': 'Pure Android experience with fantastic camera',
        'stock_quantity': 12,
        'sku': 'GOOGPX7P001',
        'color': 'Obsidian',
        'storage_variant': '128GB',
        'is_featured': True,
    },
]

created_count = 0
for prod_data in products_data:
    brand = brands.get(prod_data['brand'])
    category = categories.get(prod_data['category'])
    
    if not brand or not category:
        print(f"  Skipping {prod_data['name']}: Missing brand or category")
        continue
    
    product, created = Product.objects.get_or_create(
        sku=prod_data['sku'],
        defaults={
            'name': prod_data['name'],
            'brand': brand,
            'category': prod_data['category'],
            'model_number': prod_data['model_number'],
            'price': prod_data['price'],
            'discount_price': prod_data['discount_price'],
            'description': prod_data['description'],
            'stock_quantity': prod_data['stock_quantity'],
            'color': prod_data['color'],
            'storage_variant': prod_data['storage_variant'],
            'is_featured': prod_data['is_featured'],
            'is_active': True,
        }
    )
    
    if created:
        created_count += 1
        print(f"  ✓ Created: {product.name}")
    else:
        print(f"  - Exists: {product.name}")

print(f"\n✅ Sample data creation complete!")
print(f"Created {created_count} new products")
print(f"Total products now: {Product.objects.count()}")
print(f"Total brands: {Brand.objects.count()}")
print(f"Total categories: {Category.objects.count()}")
