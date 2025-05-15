const noDataPlugin = {
    id: 'noDataPlugin',
    afterDraw: (chart, args, options) => {
        let hasData = false;
        if (chart.data.datasets && chart.data.datasets.length > 0) {
            hasData = chart.data.datasets.some(dataset => dataset.data && dataset.data.length > 0);
        }

        if (!hasData) {
            const ctx = chart.ctx;
            const { width, height } = chart;
            const chartArea = chart.chartArea;

            const x = (chartArea ? chartArea.left + (chartArea.right - chartArea.left) / 2 : width / 2);
            const y = (chartArea ? chartArea.top + (chartArea.bottom - chartArea.top) / 2 : height / 2);

            ctx.save();
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            const pluginOptions = chart.config.options.plugins.noDataPlugin || {};
            const text = pluginOptions.text || 'No data to display'; // Default text
            const font = pluginOptions.font || '16px Arial';        // Default font
            const color = pluginOptions.color || 'rgba(100, 100, 100, 0.8)'; // Default color

            ctx.font = font;
            ctx.fillStyle = color;

            ctx.fillText(text, x, y);
            ctx.restore();
        }
    }
};

// Default is No data to display is no data
Chart.register(noDataPlugin);

const renderForecastChart = ({ targetId, datasets }) => {
    const datasetsPlots = [];
    let labels = [];

    // Assume all datasets share the same date range (use first one)
    if (datasets && datasets.length > 0) {
        const firstDatasetWithData = datasets.find(ds => ds.data && ds.data.length > 0);
        if (firstDatasetWithData) {
            labels = firstDatasetWithData.data.map(d => d.date);
        }
        datasets.forEach((dataset, index) => {
            if (dataset.data && dataset.data.length > 0) {
                datasetsPlots.push({
                    label: dataset.label || `Dataset ${index + 1}`,
                    data: dataset.data.map(d => d.value),
                    borderColor: dataset.borderColor || getRandomColor(index),
                    fill: false,
                    tension: 0.2
                });
            }
        });
    }

    const ctx = document.getElementById(targetId).getContext('2d');

    // If chart exists destory
    if (Chart.getChart(ctx)) {
        Chart.getChart(ctx).destroy();
    }
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
                },
                noDataPlugin: {
                    text: 'No trend data currently available.', // Custom message
                    font: '18px "Helvetica Neue", Helvetica, Arial, sans-serif',
                    color: '#888'
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
