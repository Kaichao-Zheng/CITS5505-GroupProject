const renderForecastChart = ({ targetId, datasets }) => {
    const datasetsPlots = [];
    
    // Assume all datasets share the same date range (use first one)
    const labels = datasets[0].data.map(d => d.date);

    datasets.forEach((dataset, index) => {
        datasetsPlots.push({
            label: dataset.label || `Dataset ${index + 1}`,
            data: dataset.data.map(d => d.value),
            borderColor: dataset.borderColor || getRandomColor(index),
            fill: false,
            tension: 0.2
        });
    });

    const ctx = document.getElementById(targetId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasetsPlots
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
};

// Optional: Random color generator (or use fixed list)
function getRandomColor(i) {
    const colors = ['#3e95cd', '#8e5ea2', '#3cba9f', '#e8c3b9', '#c45850'];
    return colors[i % colors.length];
}
