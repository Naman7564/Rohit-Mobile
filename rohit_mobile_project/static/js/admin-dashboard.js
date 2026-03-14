// Admin Dashboard JavaScript
const API_BASE_URL = '/api';

let currentProductId = null;
let selectedProductForStock = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupCameraModal();
    setupStockModal();
    setupProductForm();
    loadDashboardStats();
    loadInventory();
    loadLowStockAlerts();
    loadAllProducts();
});

// Navigation Setup
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked item
            item.classList.add('active');
            const sectionId = item.dataset.section;
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

// Camera Modal Setup
function setupCameraModal() {
    const cameraBtn = document.getElementById('camera-btn');
    const cameraModal = document.getElementById('camera-modal');
    const closeCameraBtn = document.getElementById('close-camera-btn');
    const captureBtn = document.getElementById('capture-btn');
    const retakeBtn = document.getElementById('retake-btn');
    const processBtn = document.getElementById('process-btn');
    
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');
    const preview = document.getElementById('camera-preview');
    
    let stream = null;
    let capturedImage = null;
    
    // Open camera
    cameraBtn.addEventListener('click', async () => {
        cameraModal.classList.add('show');
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment' } 
            });
            video.srcObject = stream;
        } catch (error) {
            alert('Cannot access camera: ' + error.message);
        }
    });
    
    // Capture photo
    captureBtn.addEventListener('click', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        capturedImage = canvas.toDataURL('image/jpeg');
        preview.innerHTML = `<img src="${capturedImage}" alt="Captured">`;
        
        video.style.display = 'none';
        captureBtn.style.display = 'none';
        retakeBtn.style.display = 'inline-block';
        processBtn.style.display = 'inline-block';
    });
    
    // Retake photo
    retakeBtn.addEventListener('click', () => {
        preview.innerHTML = '';
        video.style.display = 'block';
        captureBtn.style.display = 'inline-block';
        retakeBtn.style.display = 'none';
        processBtn.style.display = 'none';
    });
    
    // Process image with AI
    processBtn.addEventListener('click', async () => {
        await processImageWithAI(capturedImage);
    });
    
    // Close modal
    closeCameraBtn.addEventListener('click', () => {
        cameraModal.classList.remove('show');
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        video.style.display = 'block';
        captureBtn.style.display = 'inline-block';
        retakeBtn.style.display = 'none';
        processBtn.style.display = 'none';
        preview.innerHTML = '';
    });
    
    // Close modal when clicking X
    document.querySelector('#camera-modal .modal-close').addEventListener('click', () => {
        closeCameraBtn.click();
    });
}

// Process image with AI
async function processImageWithAI(imageData) {
    try {
        const blob = await fetch(imageData).then(r => r.blob());
        const formData = new FormData();
        formData.append('image', blob, 'product.jpg');
        
        const response = await fetch(`${API_BASE_URL}/ai/detect/`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            alert('Error detecting product');
            return;
        }
        
        const data = await response.json();
        
        // Fill form with detected data
        document.getElementById('product-name').value = data.name || '';
        document.getElementById('product-brand').value = data.brand || '';
        document.getElementById('product-category').value = data.category?.toLowerCase() || '';
        document.getElementById('product-model').value = data.model_number || '';
        document.getElementById('product-description').value = data.description || '';
        document.getElementById('product-color').value = data.color || '';
        document.getElementById('product-storage').value = data.storage_variant || '';
        
        // Close camera modal and show form
        document.getElementById('camera-modal').classList.remove('show');
        document.getElementById('add-product').classList.add('active');
        document.querySelector('[data-section="add-product"]').classList.add('active');
        
        alert('Product details auto-filled! Please review and add remaining information.');
        
    } catch (error) {
        console.error('Error processing image:', error);
        alert('Error processing image: ' + error.message);
    }
}

// Product Form Setup
function setupProductForm() {
    const form = document.getElementById('product-form');
    const imageInput = document.getElementById('product-image');
    const imagePreview = document.getElementById('image-preview');
    
    // Preview image
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                imagePreview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Submit form
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch(`${API_BASE_URL}/ai/create_from_detection/`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                alert('Product added successfully!');
                form.reset();
                imagePreview.innerHTML = '';
                loadAllProducts();
                loadDashboardStats();
            } else {
                const errors = await response.json();
                alert('Error adding product: ' + JSON.stringify(errors));
            }
        } catch (error) {
            console.error('Error adding product:', error);
            alert('Error adding product: ' + error.message);
        }
    });
    
    // Upload button
    document.getElementById('upload-btn').addEventListener('click', () => {
        imageInput.click();
    });
}

// Stock Modal Setup
function setupStockModal() {
    const stockModal = document.getElementById('stock-modal');
    const saveStockBtn = document.getElementById('save-stock-btn');
    const closeStockBtn = document.getElementById('close-stock-modal-btn');
    
    saveStockBtn.addEventListener('click', async () => {
        const productId = selectedProductForStock;
        const quantity = parseInt(document.getElementById('stock-quantity').value);
        const type = document.getElementById('stock-type').value;
        const notes = document.getElementById('stock-notes').value;
        
        try {
            const endpoint = type === 'add' ? 'add_stock' : 'remove_stock';
            const response = await fetch(`${API_BASE_URL}/inventory/${endpoint}/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity,
                    notes: notes
                })
            });
            
            if (response.ok) {
                alert('Stock updated successfully!');
                stockModal.classList.remove('show');
                loadInventory();
                loadDashboardStats();
            } else {
                alert('Error updating stock');
            }
        } catch (error) {
            console.error('Error updating stock:', error);
        }
    });
    
    closeStockBtn.addEventListener('click', () => {
        stockModal.classList.remove('show');
    });
    
    document.querySelector('#stock-modal .modal-close').addEventListener('click', () => {
        closeStockBtn.click();
    });
}

// Load dashboard stats
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const data = await response.json();
        const products = data.results || data;
        
        document.getElementById('total-products').textContent = products.length;
        
        const lowStockCount = products.filter(p => p.stock_quantity < 10).length;
        document.getElementById('low-stock-count').textContent = lowStockCount;
        
        const totalStock = products.reduce((sum, p) => sum + p.stock_quantity, 0);
        document.getElementById('total-stock').textContent = totalStock;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load inventory
async function loadInventory() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const data = await response.json();
        const products = data.results || data;
        
        const list = document.getElementById('inventory-list');
        list.innerHTML = '';
        
        products.forEach(product => {
            const item = document.createElement('div');
            item.className = 'inventory-item';
            
            const stockClass = product.stock_quantity < 10 ? 'low-stock' : '';
            
            item.innerHTML = `
                <div>
                    <img src="${product.image}" alt="${product.name}" style="width: 50px; height: 50px; border-radius: 4px; object-fit: cover;">
                </div>
                <div>
                    <p class="item-name">${product.name}</p>
                    <p class="item-sku">SKU: ${product.sku}</p>
                </div>
                <div>
                    <p class="item-price">₹${product.discount_price || product.price}</p>
                </div>
                <div>
                    <p class="item-stock ${stockClass}">${product.stock_quantity} units</p>
                </div>
                <div class="item-actions">
                    <button class="btn-stock" onclick="openStockModal(${product.id})">Update</button>
                    <button class="btn-edit" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn-delete" onclick="deleteProduct(${product.id})">Delete</button>
                </div>
            `;
            
            list.appendChild(item);
        });
        
    } catch (error) {
        console.error('Error loading inventory:', error);
    }
}

// Load low stock alerts
async function loadLowStockAlerts() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory/low_stock_alerts/`);
        const alerts = await response.json();
        
        const list = document.getElementById('alerts-list');
        list.innerHTML = '';
        
        if (alerts.length === 0) {
            list.innerHTML = '<p style="padding: 2rem; text-align: center; color: #27ae60;">✓ No low stock alerts</p>';
            return;
        }
        
        alerts.forEach(alert => {
            const item = document.createElement('div');
            item.className = 'alert-item';
            
            item.innerHTML = `
                <div>
                    <p class="item-name">${alert.product_name}</p>
                    <p class="item-sku">Threshold: ${alert.threshold}</p>
                </div>
                <div>
                    <p><strong>Current Stock: ${alert.product_stock}</strong></p>
                </div>
                <div>
                    <span class="alert-status ${alert.status}">${alert.status.toUpperCase()}</span>
                </div>
                <div class="item-actions">
                    <button class="btn-stock" onclick="openStockModal(${alert.product})">Restock Now</button>
                </div>
            `;
            
            list.appendChild(item);
        });
        
    } catch (error) {
        console.error('Error loading low stock alerts:', error);
    }
}

// Load all products
async function loadAllProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const data = await response.json();
        const products = data.results || data;
        
        const list = document.getElementById('products-list');
        list.innerHTML = '';
        
        products.forEach(product => {
            const item = document.createElement('div');
            item.className = 'product-item';
            
            item.innerHTML = `
                <div>
                    <img src="${product.image}" alt="${product.name}" style="width: 50px; height: 50px; border-radius: 4px; object-fit: cover;">
                </div>
                <div>
                    <p class="item-name">${product.name}</p>
                    <p class="item-sku">SKU: ${product.sku}</p>
                </div>
                <div>
                    <p>${product.category_display}</p>
                </div>
                <div>
                    <p class="item-price">₹${product.discount_price || product.price}</p>
                </div>
                <div>
                    <p>${product.stock_quantity} in stock</p>
                </div>
                <div class="item-actions">
                    <button class="btn-edit" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn-delete" onclick="deleteProduct(${product.id})">Delete</button>
                </div>
            `;
            
            list.appendChild(item);
        });
        
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Open stock modal
function openStockModal(productId) {
    const modal = document.getElementById('stock-modal');
    selectedProductForStock = productId;
    
    // Reset form
    document.getElementById('stock-quantity').value = '1';
    document.getElementById('stock-type').value = 'add';
    document.getElementById('stock-notes').value = '';
    
    modal.classList.add('show');
}

// Edit product (placeholder)
function editProduct(productId) {
    alert('Edit functionality to be implemented');
}

// Delete product
async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok || response.status === 204) {
            alert('Product deleted successfully!');
            loadInventory();
            loadAllProducts();
            loadDashboardStats();
        } else {
            alert('Error deleting product');
        }
    } catch (error) {
        console.error('Error deleting product:', error);
    }
}
