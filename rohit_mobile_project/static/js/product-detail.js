// Product Detail Page JavaScript
const API_BASE_URL = '/api';
let productId;

// Get product ID from URL
document.addEventListener('DOMContentLoaded', () => {
    const pathParts = window.location.pathname.split('/');
    productId = pathParts[2];
    
    if (productId) {
        loadProductDetail(productId);
        loadRelatedProducts(productId);
    }
});

// Load product detail
async function loadProductDetail(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${id}/`);
        const product = await response.json();
        
        // Update breadcrumb
        document.getElementById('breadcrumb-product').textContent = product.name;
        
        // Update images
        document.getElementById('main-image').src = product.image;
        
        // Update product info
        document.getElementById('product-name').textContent = product.name;
        document.getElementById('product-brand').textContent = product.brand ? product.brand.name : 'Unknown';
        
        // Update prices
        const displayPrice = product.discount_price || product.price;
        document.getElementById('product-price').textContent = `₹${displayPrice}`;
        
        if (product.discount_price) {
            document.getElementById('product-original-price').textContent = `₹${product.price}`;
            document.getElementById('product-discount').textContent = `${product.discount_percentage}% OFF`;
        } else {
            document.getElementById('product-original-price').style.display = 'none';
            document.getElementById('product-discount').style.display = 'none';
        }
        
        // Update stock info
        const stockInfo = document.getElementById('stock-info');
        if (product.stock_quantity > 0) {
            stockInfo.innerHTML = `<span class="stock-available">✓ In Stock (${product.stock_quantity} available)</span>`;
        } else {
            stockInfo.innerHTML = `<span class="stock-out">Out of Stock</span>`;
        }
        
        // Update specifications
        document.getElementById('spec-category').textContent = product.category_display || product.category;
        document.getElementById('spec-model').textContent = product.model_number || 'N/A';
        document.getElementById('spec-color').textContent = product.color || 'N/A';
        document.getElementById('spec-sku').textContent = product.sku;
        
        if (product.storage_variant) {
            document.getElementById('spec-storage-li').style.display = 'block';
            document.getElementById('spec-storage').textContent = product.storage_variant;
        }
        
        // Update description
        document.getElementById('product-description').textContent = product.description;
        
        // Set quantity input state
        const quantityInput = document.getElementById('quantity');
        if (product.stock_quantity <= 0) {
            quantityInput.disabled = true;
            document.getElementById('add-to-cart').disabled = true;
        }
        
    } catch (error) {
        console.error('Error loading product detail:', error);
    }
}

// Load related products
async function loadRelatedProducts(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const data = await response.json();
        
        const products = data.results || data;
        const currentProduct = products.find(p => p.id == id);
        
        if (!currentProduct) return;
        
        // Get related products (same category, exclude current)
        const related = products
            .filter(p => p.category === currentProduct.category && p.id !== id)
            .slice(0, 4);
        
        const grid = document.getElementById('related-grid');
        grid.innerHTML = '';
        
        related.forEach(product => {
            grid.appendChild(createProductCard(product));
        });
        
    } catch (error) {
        console.error('Error loading related products:', error);
    }
}

// Create product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const displayPrice = product.discount_price || product.price;
    
    card.innerHTML = `
        <img src="${product.image}" alt="${product.name}" class="product-card-image">
        <div class="product-card-body">
            <p class="product-card-brand">${product.brand_name || 'Unknown'}</p>
            <p class="product-card-name">${product.name}</p>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap;">
                <span class="product-card-price">₹${displayPrice}</span>
                ${product.discount_price ? `
                    <span class="product-card-original-price">₹${product.price}</span>
                    <span class="product-card-discount">${product.discount_percentage}% OFF</span>
                ` : ''}
            </div>
            <p class="product-card-stock">
                <span class="${product.stock_quantity > 0 ? 'stock-available' : 'stock-out'}">
                    ${product.stock_quantity > 0 ? `In Stock (${product.stock_quantity})` : 'Out of Stock'}
                </span>
            </p>
        </div>
        <div class="product-card-footer">
            <button class="btn btn-primary" onclick="window.location.href='/products/${product.id}/'">View</button>
        </div>
    `;
    
    return card;
}

// Add to cart (placeholder)
document.addEventListener('DOMContentLoaded', () => {
    const addToCartBtn = document.getElementById('add-to-cart');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', () => {
            const quantity = document.getElementById('quantity').value;
            alert(`Added ${quantity} item(s) to cart! (Cart functionality to be implemented)`);
        });
    }
});
