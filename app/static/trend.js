// Global or accessible variable to temporarily store fetched data
trendModalData = null;
let currentForecastChart = null

const handleTrendButtonClick = (productId) => {
    fetch(`${baseURL}/api/product/exists/${productId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            response.json().then(data => {
                trendModalData = data
                // addEventListener()
                newHandleEvent(data)
            })
        })
        .catch(error => {
            console.error('Error fetching data in onclick:', error);
            trendModalData = null; // Clear on error
        });
}

const newHandleEvent = (data) => {
    trendModalEle = document.getElementById('trendModalProductName');
    trendModalEle.textContent = data.product.name

    fetch(`${baseURL}/api/price_trend/${data.product.id}`)
        .then(res => res.json())
        .then(data => {
            renderForecastChart({
                targetId: 'forecast1',
                datasets: data,
                label: '7-Day Forecast',
                borderColor: 'green'
            });
        });
}