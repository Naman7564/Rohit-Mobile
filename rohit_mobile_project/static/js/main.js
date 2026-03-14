// Main Page JavaScript
const API_BASE_URL = '/api';

// Fetch featured products
async function loadFeaturedProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/featured/`);
        const data = await response.json();
        
        const container = document.getElementById('featured-products');
        container.innerHTML = '';
        
        data.forEach(product => {
            container.appendChild(createProductCard(product));
        });
    } catch (error) {
        console.error('Error loading featured products:', error);
    }
}

// Fetch latest products
async function loadLatestProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const data = await response.json();
        
        const container = document.getElementById('latest-products');
        container.innerHTML = '';
        
        // Show first 8 products
        (data.results || data).slice(0, 8).forEach(product => {
            container.appendChild(createProductCard(product));
        });
    } catch (error) {
        console.error('Error loading latest products:', error);
    }
}

// Create product card element
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const discountPercentage = product.discount_percentage || 0;
    const displayPrice = product.discount_price || product.price;
    
    card.innerHTML = `
        <img src="${product.image}" alt="${product.name}" class="product-card-image">
        <div class="product-card-body">
            <p class="product-card-brand">${product.brand_name || 'Unknown'}</p>
            <p class="product-card-name">${product.name}</p>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span class="product-card-price">₹${displayPrice}</span>
                ${product.discount_price ? `
                    <span class="product-card-original-price">₹${product.price}</span>
                    <span class="product-card-discount">${discountPercentage}% OFF</span>
                ` : ''}
            </div>
            <p class="product-card-stock">
                <span class="${product.stock_quantity > 0 ? 'stock-available' : 'stock-out'}">
                    ${product.stock_quantity > 0 ? `In Stock (${product.stock_quantity})` : 'Out of Stock'}
                </span>
            </p>
        </div>
        <div class="product-card-footer">
            <button class="btn btn-primary" onclick="window.location.href='/products/${product.id}/'">View Details</button>
        </div>
    `;
    
    return card;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadFeaturedProducts();
    loadLatestProducts();
});
