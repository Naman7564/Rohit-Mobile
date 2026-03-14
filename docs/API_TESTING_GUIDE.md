# API Testing Guide

## Testing Rohit Mobile API

This guide provides examples and test cases for all API endpoints.

## Prerequisites

- Running Rohit Mobile instance (Docker or local)
- API testing tool (Postman, cURL, or Thunder Client)
- Sample product data loaded

## Base URL

```
http://localhost        # Docker
http://localhost:8000   # Local development
```

---

## Product Endpoints

### 1. Get All Products

**Request:**
```http
GET /api/products/
```

**cURL:**
```bash
curl http://localhost/api/products/
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Samsung Galaxy S23",
      "brand_name": "Samsung",
      "category": "mobile",
      "price": "99999.00",
      "discount_price": "79999.00",
      "image": "/media/products/s23.jpg",
      "stock_quantity": 15,
      "discount_percentage": 20.0,
      "is_featured": true,
      "created_at": "2026-03-14T10:00:00Z"
    }
  ]
}
```

### 2. Get Single Product

**Request:**
```http
GET /api/products/1/
```

**cURL:**
```bash
curl http://localhost/api/products/1/
```

**Response:**
```json
{
  "id": 1,
  "name": "Samsung Galaxy S23",
  "brand": {
    "id": 1,
    "name": "Samsung",
    "logo": "/media/brands/samsung.png",
    "description": "Samsung products"
  },
  "category": "mobile",
  "category_display": "Mobile Phone",
  "model_number": "SM-S911B",
  "price": "99999.00",
  "discount_price": "79999.00",
  "description": "Premium smartphone with AMOLED display...",
  "image": "/media/products/s23.jpg",
  "stock_quantity": 15,
  "sku": "SGS23-001",
  "color": "Phantom Black",
  "storage_variant": "256GB",
  "created_at": "2026-03-14T10:00:00Z",
  "updated_at": "2026-03-14T10:00:00Z",
  "is_active": true,
  "is_featured": true,
  "additional_images": [],
  "discount_percentage": 20.0,
  "is_low_stock": false
}
```

### 3. Get Featured Products

**Request:**
```http
GET /api/products/featured/
```

**cURL:**
```bash
curl http://localhost/api/products/featured/
```

**Response:** (List of featured products only)

### 4. Filter Products

**By Category:**
```http
GET /api/products/?category=mobile
```

**By Brand ID:**
```http
GET /api/products/?brand=1
```

**By Search:**
```http
GET /api/products/?search=samsung
```

**By Price (Limit passed in frontend):**
```http
GET /api/products/
```

**Combined:**
```http
GET /api/products/?category=mobile&brand=1&search=galaxy
```

### 5. Get Categories

**Request:**
```http
GET /api/products/categories/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Mobile Phone",
    "slug": "mobile",
    "description": "",
    "icon": "📱"
  }
]
```

### 6. Get Brands

**Request:**
```http
GET /api/products/brands/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Samsung",
    "logo": "/media/brands/samsung.png",
    "description": "Samsung products"
  }
]
```

### 7. Create Product

**Request:**
```http
POST /api/ai/create_from_detection/
Content-Type: multipart/form-data

name=Samsung+Galaxy+S24&brand=1&category=mobile&price=99999&discount_price=79999&stock_quantity=10&sku=SGS24-001&image=<file>
```

**cURL:**
```bash
curl -X POST http://localhost/api/ai/create_from_detection/ \
  -F "name=Samsung Galaxy S24" \
  -F "brand=1" \
  -F "category=mobile" \
  -F "price=99999" \
  -F "discount_price=79999" \
  -F "stock_quantity=10" \
  -F "sku=SGS24-001" \
  -F "image=@/path/to/image.jpg"
```

**Response:**
```json
{
  "name": "Samsung Galaxy S24",
  "brand": 1,
  "category": "mobile",
  "model_number": "",
  "price": "99999.00",
  "discount_price": "79999.00",
  "description": "",
  "image": "/media/products/...",
  "stock_quantity": 10,
  "sku": "SGS24-001",
  "color": "",
  "storage_variant": "",
  "is_active": true,
  "is_featured": false
}
```

---

## AI Detection Endpoints

### 1. Detect Product from Image

**Request:**
```http
POST /api/ai/detect/
Content-Type: multipart/form-data

image=<image_file>
```

**cURL:**
```bash
curl -X POST http://localhost/api/ai/detect/ \
  -F "image=@/path/to/phone_image.jpg"
```

**Response:**
```json
{
  "name": "Samsung Galaxy S23",
  "brand": "Samsung",
  "category": "Mobile Phone",
  "model_number": "SM-S911B",
  "description": "Flagship Android smartphone with AMOLED display and triple camera",
  "color": "Black",
  "storage_variant": "256GB"
}
```

**Testing with Python:**
```python
import requests

files = {'image': open('phone.jpg', 'rb')}
response = requests.post('http://localhost/api/ai/detect/', files=files)
print(response.json())
```

### 2. Error Handling

**Missing Image:**
```json
{
  "error": "Image file is required"
}
```

**Invalid Image:**
```json
{
  "error": "Failed to detect product from image"
}
```

**API Error:**
```json
{
  "error": "Error processing image: [specific error]"
}
```

---

## Inventory Endpoints

### 1. Add Stock

**Request:**
```http
POST /api/inventory/add_stock/
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 10,
  "notes": "Stock received from supplier"
}
```

**cURL:**
```bash
curl -X POST http://localhost/api/inventory/add_stock/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 10,
    "notes": "Stock received"
  }'
```

**Response:**
```json
{
  "id": 1,
  "product": 1,
  "product_name": "Samsung Galaxy S23",
  "transaction_type": "add",
  "quantity": 10,
  "notes": "Stock received from supplier",
  "created_by": "admin",
  "created_at": "2026-03-14T10:15:00Z"
}
```

### 2. Remove Stock

**Request:**
```http
POST /api/inventory/remove_stock/
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2,
  "notes": "Damaged units"
}
```

**Response:** (Similar to add_stock)

### 3. Get Low Stock Alerts

**Request:**
```http
GET /api/inventory/low_stock_alerts/
```

**Response:**
```json
[
  {
    "id": 1,
    "product": 1,
    "product_name": "Samsung Galaxy S23",
    "product_image": "/media/products/s23.jpg",
    "product_stock": 5,
    "threshold": 10,
    "status": "pending",
    "created_at": "2026-03-14T09:00:00Z",
    "acknowledged_at": null,
    "resolved_at": null
  }
]
```

### 4. Get All Transactions

**Request:**
```http
GET /api/inventory/
```

**Filter by Product:**
```http
GET /api/inventory/?product_id=1
```

**Filter by Type:**
```http
GET /api/inventory/?type=add
```

---

## Postman Collection

### Import this into Postman

```json
{
  "info": {
    "name": "Rohit Mobile API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Products",
      "item": [
        {
          "name": "Get All Products",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/products/"
          }
        },
        {
          "name": "Get Product Detail",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/products/1/"
          }
        },
        {
          "name": "Get Featured",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/api/products/featured/"
          }
        }
      ]
    },
    {
      "name": "AI Detection",
      "item": [
        {
          "name": "Detect Product",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/ai/detect/",
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "image",
                  "type": "file",
                  "src": "path/to/image.jpg"
                }
              ]
            }
          }
        }
      ]
    },
    {
      "name": "Inventory",
      "item": [
        {
          "name": "Add Stock",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/inventory/add_stock/",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"product_id\": 1,\n  \"quantity\": 10,\n  \"notes\": \"Stock received\"\n}"
            }
          }
        }
      ]
    }
  ]
}
```

---

## Testing with Python

### Install dependencies:
```bash
pip install requests
```

### Test script:
```python
import requests
import json

BASE_URL = "http://localhost/api"

def test_products():
    """Test product endpoints"""
    print("Testing Products API...")
    
    # Get all products
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Status: {response.status_code}")
    print(f"Products: {response.json()['count']}")
    
    # Get featured
    response = requests.get(f"{BASE_URL}/products/featured/")
    print(f"Featured: {len(response.json())}")

def test_ai_detection(image_path):
    """Test AI detection"""
    print("Testing AI Detection...")
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"{BASE_URL}/ai/detect/", files=files)
    
    print(f"Status: {response.status_code}")
    print(f"Result: {json.dumps(response.json(), indent=2)}")

def test_inventory():
    """Test inventory endpoints"""
    print("Testing Inventory API...")
    
    data = {
        "product_id": 1,
        "quantity": 5,
        "notes": "Test"
    }
    
    response = requests.post(f"{BASE_URL}/inventory/add_stock/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Transaction: {response.json()}")

# Run tests
if __name__ == "__main__":
    test_products()
    test_inventory()
    # test_ai_detection("phone.jpg")
```

---

## Performance Testing

### Load Test with Python:
```python
import time
import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost/api"
NUM_REQUESTS = 100

def make_request(i):
    start = time.time()
    response = requests.get(f"{BASE_URL}/products/")
    elapsed = time.time() - start
    return elapsed

# Run concurrent requests
with ThreadPoolExecutor(max_workers=10) as executor:
    times = list(executor.map(make_request, range(NUM_REQUESTS)))

print(f"Average response time: {sum(times) / len(times):.3f}s")
print(f"Min: {min(times):.3f}s, Max: {max(times):.3f}s")
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Deletion successful |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal error |

---

## Rate Limiting

- API endpoints: 10 requests/second
- General endpoints: 30 requests/second

Response headers will include remaining requests:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1234567890
```

---

## Debugging Tips

1. **Check Status Code**: Always check HTTP status first
2. **Review Response**: Look for error messages in JSON
3. **Check Logs**: `docker-compose logs web`
4. **Verify Data**: Ensure product exists before testing
5. **Test Offline**: Use sample data first
6. **Enable Verbose Mode**: Add logging for debugging

---

**Created**: March 14, 2026
**Last Updated**: March 14, 2026
