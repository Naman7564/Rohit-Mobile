# Quick Start Guide - Rohit Mobile

## 🚀 Get Started in 5 Minutes

### Step 1: Clone/Download Project
```bash
cd "Rohit Mobile"
```

### Step 2: Setup Environment Variables
```bash
# Copy example to .env
cp .env.example .env

# Edit .env and add your AI API key
# Choose one:
# - OpenAI: https://platform.openai.com/api-keys
# - Google: https://makersuite.google.com/app/apikey
# - Anthropic: https://console.anthropic.com/
```

### Step 3: Start with Docker (Easiest)
```bash
docker-compose up -d --build
```

### Step 4: Create Admin Account
```bash
docker-compose exec web python manage.py createsuperuser
# Enter username, email, and password when prompted
```

### Step 5: Access the Application
- 🛒 **Customer Site**: http://localhost
- 👨‍💼 **Admin Dashboard**: http://localhost/admin-dashboard/
- 🔐 **Django Admin**: http://localhost/admin/ (use superuser credentials)
- 📡 **API Docs**: http://localhost/api/products/

---

## 📱 Features to Try

### 1. Add Product with AI Camera
1. Go to Admin Dashboard: http://localhost/admin-dashboard/
2. Click "Add Product" → "Add Using Camera"
3. Take a photo of a phone/accessory
4. AI will auto-detect and fill product details
5. Add price, stock, and save

### 2. Browse Products
1. Visit: http://localhost
2. Click "Shop Now" or go to Products
3. Filter by category, brand, or price
4. Click "View Details" for full product info

### 3. Manage Inventory
1. Go to Admin Dashboard
2. Click "Inventory Management"
3. Update stock levels
4. View low stock alerts

---

## 🛠️ Development Setup (No Docker)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your API key

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Start dev server
python manage.py runserver

# Visit: http://localhost:8000
```

---

## 📚 Database Management

### Add Sample Data

```python
# In Django shell
python manage.py shell

# Create brands
from products.models import Brand
Brand.objects.create(name="Samsung")
Brand.objects.create(name="iPhone")
Brand.objects.create(name="OnePlus")

# Exit
exit()
```

### Backup Database
```bash
# SQLite
cp rohit_mobile_project/db.sqlite3 backup.sqlite3

# Docker
docker-compose exec web cp db.sqlite3 /app/media/db_backup.sqlite3
```

---

## 🔧 Common Commands

### Docker Commands
```bash
# Restart services
docker-compose restart

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Remove everything (careful!)
docker-compose down -v
```

### Django Commands
```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check

# Database shell
python manage.py shell
```

---

## 🔑 API Endpoints Quick Reference

### Products
- `GET /api/products/` - All products
- `GET /api/products/featured/` - Featured only
- `GET /api/products/{id}/` - Product details
- `GET /api/products/?category=mobile` - Filter by category

### AI Detection
- `POST /api/ai/detect/` - Detect product from image
- `POST /api/ai/create_from_detection/` - Create product with details

### Inventory
- `POST /api/inventory/add_stock/` - Add stock
- `POST /api/inventory/remove_stock/` - Remove stock
- `GET /api/inventory/low_stock_alerts/` - Low stock alerts

---

## ⚡ Performance Tips

1. **Cache Static Files**: Already configured
2. **Use Pagination**: Automatically limited to 12 items per page
3. **Compress Media**: Use quality 8-9 JPEGs
4. **Enable GZIP**: Already configured in Nginx
5. **Database Indexes**: Already created on frequently queried fields

---

## 🔒 Security Setup (Production)

1. **Generate Secret Key**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Enable HTTPS**
   - Get SSL certificate (Let's Encrypt)
   - Configure in Nginx

3. **Set DEBUG=False**
   - Edit `.env`: `DEBUG=False`

4. **Configure Allowed Hosts**
   - Edit `.env`: `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`

---

## 📞 Support

**Issues?**
1. Check logs: `docker-compose logs web`
2. Verify .env file is configured
3. Ensure API key is valid
4. Check firewall/port settings

**For Help:**
- Read full README.md
- Check Django logs
- Review API response errors

---

## 🎯 Next Steps

1. ✅ Add more products via camera or admin
2. ✅ Customize CSS for branding
3. ✅ Add payment gateway
4. ✅ Set up email notifications
5. ✅ Deploy to production

---

**Happy coding! 🚀**
