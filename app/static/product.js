const mockProducts = [
    { name: "Mock Product 1" },
    { name: "Mock Product 2" },
    { name: "Mock Product 3" },
    { name: "Mock Product 4" },
    { name: "Mock Product 5" },
    { name: "Mock Product 6" },
    { name: "Mock Product 7" },
    { name: "Mock Product 8" }
];

let loaded = 0;

function loadMore(count = 6) {
    const container = document.getElementById('product-list');
    for (let i = loaded; i < loaded + count && i < mockProducts.length; i++) {
    const card = document.createElement('div');
    card.className = 'col-md-6 col-lg-4';
    card.innerHTML = `
        <div class="product-card">
            <div class="product-img">🖼</div>
            <p class="mt-2 mb-1">${mockProducts[i].name}</p>
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
}

window.onload = () => loadMore();