let loaded = 0;

function loadMore(count = 6) {
    const container = document.getElementById('product-list');
    
    // send AJAX request to the backend to get product data 
    $.ajax({
        url: '/api/products',  
        method: 'GET',
        success: function(products) {
            for (let i = loaded; i < loaded + count && i < products.length; i++) {
                const card = document.createElement('div');
                card.className = 'col-md-6 col-lg-4';
                card.innerHTML = `
                    <div class="product-card">
                        <div class="product-img">
                            <img src="/static/img/mock-image.png" alt="${products[i].name}" class="img-fluid w-100" style="max-height: 360px; object-fit: contain;">
                        </div>
                        <p class="mt-2 mb-1">${products[i].name}</p>
                        <span class="badge bg-success">Shop</span>
                        <a class="btn btn-sm btn-primary float-end"
                            href="#"
                            data-bs-toggle="modal"
                            data-bs-target="#trendModal">
                            View Trend
                        </a>
                        <p class="mt-1 mb-0 text-white-50 small">&lt; Vendor with lowest price NOW &gt;</p>
                    </div>
                `;
                container.appendChild(card);
            }
            loaded += count;
        },
        error: function(error) {
            console.error('Error fetching products:', error);
            alert('Failed to load products. Please try again later.');
        }
    });
}

window.onload = () => loadMore();
