# Rohit Mobile - E-Commerce Catalog & Inventory Management System

🚀 A full-stack ecommerce platform for mobile phones and accessories with AI-powered product detection, inventory management, and admin dashboard.

## Features

### 🛒 Customer Features
- **Product Catalog**: Browse mobile phones, chargers, cables, earbuds, and accessories
- **Responsive Design**: Mobile-friendly interface
- **Product Filtering**: Filter by category, brand, and price
- **Product Details**: Comprehensive product information with images
- **Search**: Quick product search functionality

### 👨‍💼 Admin Features
- **AI Camera Product Entry**: Add products using mobile camera with AI detection
- **Inventory Management**: Track stock levels in real-time
- **Low Stock Alerts**: Get notified when inventory is running low
- **Product Management**: Edit, delete, and manage products
- **Dashboard**: Quick overview of inventory and sales statistics

### 🤖 AI Integration
- **Vision API Support**: OpenAI, Google Gemini, and Anthropic Claude
- **Auto Product Detection**: Automatically extract product details from images
- **Smart Categorization**: AI-powered product categorization

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite3 (easily upgradable to PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **App Server**: Gunicorn
- **AI**: OpenAI Vision, Google Gemini, Anthropic Claude APIs

## Project Structure

```
rohit_mobile/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── .env
├── .env.example
├── nginx/
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
├── rohit_mobile_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── products/
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── apps.py
│   ├── inventory/
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── apps.py
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── apps.py
│   ├── ai_services/
│   │   └── detector.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   └── admin-dashboard.css
│   │   └── js/
│   │       ├── main.js
│   │       ├── products.js
│   │       ├── product-detail.js
│   │       └── admin-dashboard.js
│   ├── templates/
│   │   ├── index.html
│   │   ├── products.html
│   │   ├── product_detail.html
│   │   └── admin_dashboard.html
│   └── media/
└── README.md
```

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Python 3.11+ (for local development)
- An API key from OpenAI, Google Gemini, or Anthropic Claude

### Setup with Docker (Recommended)

1. **Clone/Download the project**
   ```bash
   cd "Rohit Mobile"
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Build and start containers**
   ```bash
   docker-compose up -d --build
   ```

4. **Create superuser for admin panel**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - Customer Site: http://localhost
   - Admin Dashboard: http://localhost/admin-dashboard/
   - Django Admin: http://localhost/admin/
   - API: http://localhost/api/

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Customer Site: http://localhost:8000
   - Admin Dashboard: http://localhost:8000/admin-dashboard/
   - Django Admin: http://localhost:8000/admin/
   - API: http://localhost:8000/api/

## API Documentation

### Product Endpoints

#### Get All Products
```http
GET /api/products/
```

Query Parameters:
- `category`: Filter by category (mobile, charger, cable, earbuds, accessories)
- `brand`: Filter by brand ID
- `search`: Search by name
- `featured`: Get featured products only (true/false)

#### Get Product Details
```http
GET /api/products/{id}/
```

#### Get Featured Products
```http
GET /api/products/featured/
```

#### Get Categories
```http
GET /api/products/categories/
```

#### Get Brands
```http
GET /api/products/brands/
```

### AI Detection Endpoints

#### Detect Product from Image
```http
POST /api/ai/detect/
Content-Type: multipart/form-data

image: <image file>
```

**Response:**
```json
{
  "name": "Samsung Galaxy S23",
  "brand": "Samsung",
  "category": "Mobile",
  "model_number": "SM-S911B",
  "description": "Latest flagship smartphone",
  "color": "Black",
  "storage_variant": "128GB"
}
```

#### Create Product from Detection
```http
POST /api/ai/create_from_detection/
Content-Type: multipart/form-data

image: <image file>
name: "Samsung Galaxy S23"
brand: 1
category: "mobile"
price: 79999
discount_price: 69999
stock_quantity: 10
sku: "SGS23-128GB-BLK"
...
```

### Inventory Endpoints

#### Add Stock
```http
POST /api/inventory/add_stock/

{
  "product_id": 1,
  "quantity": 10,
  "notes": "Stock received from supplier"
}
```

#### Remove Stock
```http
POST /api/inventory/remove_stock/

{
  "product_id": 1,
  "quantity": 5,
  "notes": "Damaged units"
}
```

#### Get Low Stock Alerts
```http
GET /api/inventory/low_stock_alerts/
```

## Camera Integration

### Camera Access
The admin dashboard uses the Web Camera API (getUserMedia) to:
1. Open device camera
2. Capture product image
3. Send to AI for detection
4. Auto-fill product form

### Browser Support
- Chrome/Chromium: ✅
- Firefox: ✅
- Safari: ⚠️ (Limited HTTPS required)
- Edge: ✅

**Note:** Camera access requires HTTPS in production (except localhost for development)

## AI Providers Configuration

### OpenAI Vision API
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### Google Gemini
```env
AI_PROVIDER=google
GOOGLE_API_KEY=AIzaSy...
```

### Anthropic Claude
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

## Database Models

### Product Model
- `name`: Product name
- `brand`: Foreign key to Brand
- `category`: Product category
- `model_number`: Model identifier
- `price`: Regular price
- `discount_price`: Discounted price
- `description`: Product description
- `image`: Product image
- `stock_quantity`: Available stock
- `sku`: Stock Keeping Unit
- `color`: Product color
- `storage_variant`: For phones (128GB, 256GB, etc.)
- `is_active`: Product visibility
- `is_featured`: Featured product flag
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### InventoryTransaction Model
- `product`: Foreign key to Product
- `transaction_type`: add, remove, sale, return, damage, adjustment
- `quantity`: Transaction quantity
- `notes`: Transaction notes
- `created_by`: User who made transaction
- `created_at`: Transaction timestamp

### LowStockAlert Model
- `product`: Foreign key to Product
- `threshold`: Low stock threshold
- `status`: pending, acknowledged, resolved
- `created_at`: Alert creation time
- `acknowledged_at`: When alert was acknowledged
- `resolved_at`: When alert was resolved

## Docker Deployment

### Building Images
```bash
docker-compose build
```

### Starting Services
```bash
docker-compose up -d
```

### Stopping Services
```bash
docker-compose down
```

### Viewing Logs
```bash
docker-compose logs -f web
```

### Rebuilding After Changes
```bash
docker-compose up -d --build
```

## Production Deployment

### Environment Setup
1. Create `.env` with production settings
2. Set `DEBUG=False`
3. Generate secure `SECRET_KEY`
4. Configure allowed hosts
5. Set up SSL certificates for Nginx

### Security Checklist
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure secure cookies
- [ ] Set SECURE_SSL_REDIRECT=True
- [ ] Enable HSTS headers
- [ ] Use environment variables for secrets

### Database Migration to PostgreSQL
Replace the `db` service in `docker-compose.yml`:

```yaml
db:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: rohit_mobile
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: secure_password
  volumes:
    - postgres_volume:/var/lib/postgresql/data
```

And update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rohit_mobile',
        'USER': 'postgres',
        'PASSWORD': 'secure_password',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

## Common Issues & Troubleshooting

### Camera Not Working
- Ensure HTTPS is enabled (or localhost for development)
- Check browser permissions
- Verify `getUserMedia` support in browser

### AI Detection Failing
- Verify API key is correct
- Check API rate limits
- Ensure image format is supported (JPEG/PNG)
- Check network connectivity

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Errors
```bash
docker-compose exec web python manage.py migrate
```

### Port Already in Use
Change port in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Use 8080 instead of 8000
```

## Performance Optimization

### Caching
- Static files cached for 30 days
- Media files cached for 7 days

### Database Optimization
- Indexes on frequently queried fields
- Pagination enabled (12 items per page)

### API Rate Limiting
- General endpoints: 30 req/s
- API endpoints: 10 req/s
- Burst allowed

## Future Enhancements

- [ ] User authentication & profiles
- [ ] Shopping cart & checkout
- [ ] Payment gateway integration
- [ ] Order management system
- [ ] Customer reviews & ratings
- [ ] Email notifications
- [ ] SMS alerts for low stock
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support, email: support@rohitmobile.com

Or create an issue in the repository.

## Database Backup

### SQLite Backup
```bash
docker-compose exec web cp db.sqlite3 /app/media/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

### Restore Backup
```bash
docker-compose exec web cp /app/media/db_backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

## Maintenance

### Regular Tasks
- Monitor disk space for media files
- Review and clean up old transactions
- Update dependencies monthly
- Test backups regularly
- Monitor API usage

## Version History

### v1.0.0 (Current)
- Initial release
- Core features implemented
- Docker deployment ready
- AI product detection working
- Admin dashboard functional

---

**Created by**: Development Team  
**Last Updated**: March 14, 2026  
**Version**: 1.0.0
