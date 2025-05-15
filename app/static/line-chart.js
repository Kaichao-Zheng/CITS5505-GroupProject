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


const renderCombinedForecastChart = ({
    targetId,
    datasets: inputDatasets,
    numPredictionPoints = 3, // Number of future points to predict
    predictionLineStyle = [5, 5], // Dashed line for predictions [dashLength, spaceLength]
    forecastColor = '#FF6384', // Pinkish color for the forecast line (Chart.js red)
    aggregatedActualColor = '#AAAAAA', // Neutral color for the aggregated historical trend
    tension = 0.2 // Line tension (0 for straight, >0 for curved)
}) => {
    const allProcessedDates = new Set(); // To collect all unique dates for the x-axis

    // 1. Aggregate data from all input datasets
    const aggregatedDataValuesByDate = new Map(); // Stores { sum, count } for each date

    if (inputDatasets && inputDatasets.length > 0) {
        inputDatasets.forEach(originalDataset => {
            if (originalDataset && originalDataset.data && originalDataset.data.length > 0) {
                originalDataset.data.forEach(dp => {
                    if (dp && dp.date && dp.value !== null && dp.value !== undefined) {
                        // Ensure date is in YYYY-MM-DD format for consistent mapping
                        const cleanDate = dp.date.split('T')[0]; // Handle potential ISO strings
                        allProcessedDates.add(cleanDate);
                        const existing = aggregatedDataValuesByDate.get(cleanDate) || { sum: 0, count: 0 };
                        existing.sum += dp.value;
                        existing.count++;
                        aggregatedDataValuesByDate.set(cleanDate, existing);
                    }
                });
            }
        });
    }

    // 2. Create source points for the aggregated historical trend
    const historicalAggregatedSourcePoints = [];
    // Sort dates chronologically before processing for the historical line
    const sortedHistoricalDates = Array.from(allProcessedDates).sort((a, b) => new Date(a) - new Date(b));

    sortedHistoricalDates.forEach(date => {
        const aggData = aggregatedDataValuesByDate.get(date);
        if (aggData && aggData.count > 0) {
            historicalAggregatedSourcePoints.push({ date: date, value: (aggData.sum / aggData.count) });
        }
    });

    const datasetsForChartJS = [];

    // Add aggregated historical data line if available
    if (historicalAggregatedSourcePoints.length > 0) {
        datasetsForChartJS.push({
            label: 'Aggregated Trend',
            _sourcePoints: [...historicalAggregatedSourcePoints], // Store raw points temporarily
            borderColor: aggregatedActualColor,
            backgroundColor: aggregatedActualColor, // For point color if visible
            fill: false,
            tension: tension,
            pointRadius: 2,
            pointHoverRadius: 5,
            borderWidth: 2,
            order: 0 // Draw this line first
        });

        // 3. Generate a single prediction based on the aggregated trend
        const actualValuesOnly = historicalAggregatedSourcePoints.map(d => d.value);
        const averageOverallValue = actualValuesOnly.reduce((sum, val) => sum + val, 0) / actualValuesOnly.length;

        const lastActualPoint = historicalAggregatedSourcePoints[historicalAggregatedSourcePoints.length - 1];
        let lastDateForPrediction = lastActualPoint.date;

        let dateIntervalDays = 7; // Default interval
        if (historicalAggregatedSourcePoints.length > 1) {
            const date1 = new Date(historicalAggregatedSourcePoints[historicalAggregatedSourcePoints.length - 2].date);
            const date2 = new Date(lastActualPoint.date);
            const diffTime = Math.abs(date2.getTime() - date1.getTime());
            const inferredInterval = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            if (inferredInterval > 0) dateIntervalDays = inferredInterval;
        }

        const predictionSourcePoints = [];
        // Start prediction line connected to the last actual aggregated point
        predictionSourcePoints.push({ date: lastDateForPrediction, value: lastActualPoint.value });

        for (let i = 0; i < numPredictionPoints; i++) {
            lastDateForPrediction = addDaysToDate(lastDateForPrediction, dateIntervalDays);
            allProcessedDates.add(lastDateForPrediction); // Add new future dates for x-axis scale
            predictionSourcePoints.push({ date: lastDateForPrediction, value: averageOverallValue });
        }

        datasetsForChartJS.push({
            label: 'Overall Forecast',
            _sourcePoints: predictionSourcePoints, // Store raw points temporarily
            borderColor: forecastColor, // The requested pinkish color
            backgroundColor: forecastColor, // For point color
            borderDash: predictionLineStyle,
            fill: false,
            tension: tension,
            pointRadius: 2,
            pointHoverRadius: 5,
            borderWidth: 2,
            order: 1 // Draw this line second
        });
    }

    // 4. Finalize Chart.js data structure by aligning all points to a common set of labels
    const sortedChartLabels = Array.from(allProcessedDates).sort((a, b) => new Date(a) - new Date(b));

    const finalChartJSDatasets = datasetsForChartJS.map(ds => {
        const dataMap = new Map((ds._sourcePoints || []).map(p => [p.date, p.value]));
        // Remove our temporary _sourcePoints property before passing to Chart.js
        const { _sourcePoints, ...chartDatasetProperties } = ds;
        return {
            ...chartDatasetProperties,
            data: sortedChartLabels.map(labelDate => dataMap.get(labelDate) === undefined ? null : dataMap.get(labelDate)),
        };
    });

    // 5. Render chart
    const canvas = document.getElementById(targetId);
    if (!canvas) {
        console.error(`Canvas element with id "${targetId}" not found.`);
        return;
    }
    const ctx = canvas.getContext('2d');

    const existingChart = Chart.getChart(ctx); // Or Chart.getChart(targetId)
    if (existingChart) {
        existingChart.destroy();
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedChartLabels,
            datasets: finalChartJSDatasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                },
                noDataPlugin: { // Options for your noDataPlugin
                    text: 'No combined trend data available.', // Customized text
                    font: '18px "Helvetica Neue", Helvetica, Arial, sans-serif',
                    color: '#888'
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'MMM dd, yyyy', // Format for tooltips
                        displayFormats: {
                            day: 'MMM dd' // Format for x-axis labels
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true, // Consider if this is always appropriate for price data
                    title: {
                        display: true,
                        text: 'Average Value' // Updated Y-axis title
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false,
            }
        }
    });
};

function addDaysToDate(dateString, days) {
    const date = new Date(dateString);
    date.setDate(date.getDate() + days);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}