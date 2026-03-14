// Products Page JavaScript
const API_BASE_URL = '/api';
let allProducts = [];
let filteredProducts = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    setupEventListeners();
    loadBrands();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('search-products').addEventListener('input', filterProducts);
    document.getElementById('sort-products').addEventListener('change', sortProducts);
    document.querySelectorAll('.category-filter').forEach(checkbox => {
        checkbox.addEventListener('change', filterProducts);
    });
    document.getElementById('price-range').addEventListener('input', (e) => {
        document.getElementById('price-value').textContent = e.target.value;
        filterProducts();
    });
    document.getElementById('apply-filters').addEventListener('click', filterProducts);
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

// Load all products
async function loadProducts() {
    try {
        document.getElementById('loading').style.display = 'block';
        const response = await fetch(`${API_BASE_URL}/products/`);
        const data = await response.json();
        
        allProducts = data.results || data;
        filteredProducts = [...allProducts];
        
        displayProducts(filteredProducts);
        document.getElementById('loading').style.display = 'none';
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('loading').style.display = 'none';
    }
}

// Load brands
async function loadBrands() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/brands/`);
        const brands = await response.json();
        
        const brandList = document.getElementById('brand-list');
        brandList.innerHTML = '';
        
        brands.forEach(brand => {
            const label = document.createElement('label');
            label.innerHTML = `<input type="checkbox" class="brand-filter" value="${brand.id}"> ${brand.name}`;
            label.querySelector('input').addEventListener('change', filterProducts);
            brandList.appendChild(label);
        });
    } catch (error) {
        console.error('Error loading brands:', error);
    }
}

// Filter products
async function filterProducts() {
    const searchTerm = document.getElementById('search-products').value.toLowerCase();
    const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked')).map(c => c.value);
    const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked')).map(c => c.value);
    const maxPrice = parseInt(document.getElementById('price-range').value);
    
    filteredProducts = allProducts.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) || 
                            product.brand_name.toLowerCase().includes(searchTerm);
        const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(product.category);
        const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(product.brand.toString());
        const matchesPrice = product.price <= maxPrice;
        
        return matchesSearch && matchesCategory && matchesBrand && matchesPrice;
    });
    
    displayProducts(filteredProducts);
}

// Sort products
function sortProducts() {
    const sortValue = document.getElementById('sort-products').value;
    
    switch(sortValue) {
        case 'price-low':
            filteredProducts.sort((a, b) => (a.discount_price || a.price) - (b.discount_price || b.price));
            break;
        case 'price-high':
            filteredProducts.sort((a, b) => (b.discount_price || b.price) - (a.discount_price || a.price));
            break;
        case 'name':
            filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'latest':
        default:
            filteredProducts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }
    
    displayProducts(filteredProducts);
}

// Display products
function displayProducts(products) {
    const grid = document.getElementById('products-grid');
    const noProducts = document.getElementById('no-products');
    
    grid.innerHTML = '';
    
    if (products.length === 0) {
        noProducts.style.display = 'block';
        return;
    }
    
    noProducts.style.display = 'none';
    
    products.forEach(product => {
        grid.appendChild(createProductCard(product));
    });
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
            <button class="btn btn-primary" onclick="viewProductDetail(${product.id})">View Details</button>
        </div>
    `;
    
    return card;
}

// View product detail
function viewProductDetail(productId) {
    window.location.href = `/products/${productId}/`;
}

// Reset filters
function resetFilters() {
    document.getElementById('search-products').value = '';
    document.getElementById('price-range').value = '100000';
    document.getElementById('price-value').textContent = '100000';
    document.querySelectorAll('.category-filter').forEach(c => c.checked = false);
    document.querySelectorAll('.brand-filter').forEach(c => c.checked = false);
    document.getElementById('sort-products').value = 'latest';
    
    filteredProducts = [...allProducts];
    displayProducts(filteredProducts);
}
