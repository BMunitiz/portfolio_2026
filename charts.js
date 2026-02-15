// Chart.js initialization for portfolio visualizations
document.addEventListener('DOMContentLoaded', function() {
    // Function to create a chart if container exists
    function createChart(containerId, chartType, data, options) {
        const container = document.getElementById(containerId);
        if (container && typeof Chart !== 'undefined') {
            // Create a canvas element inside the container
            const canvas = document.createElement('canvas');
            container.appendChild(canvas);

            new Chart(canvas, {
                type: chartType,
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: options.title || ''
                        },
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: options.beginAtZero || false,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        }
                    }
                }
            });
        }
    }

    // Sample data for demonstration purposes
    const sampleData = {
        // LSTM Prediction Chart Data
        predictionData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Actual Prices',
                data: [45, 48, 52, 49, 55, 58, 60, 57, 54, 52, 49, 47],
                borderColor: '#414833',
                backgroundColor: 'rgba(65, 72, 51, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Predicted Prices',
                data: [46, 47, 51, 50, 54, 57, 59, 58, 55, 53, 50, 48],
                borderColor: '#A4AC86',
                backgroundColor: 'rgba(164, 172, 134, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },

        // LSTM Loss Chart Data
        lossData: {
            labels: ['Epoch 1', 'Epoch 10', 'Epoch 20', 'Epoch 30', 'Epoch 40', 'Epoch 50', 'Epoch 60', 'Epoch 70', 'Epoch 80', 'Epoch 90', 'Epoch 100', 'Epoch 110', 'Epoch 120'],
            datasets: [{
                label: 'Training Loss',
                data: [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.65, 0.6, 0.55, 0.52, 0.5, 0.48, 0.45],
                borderColor: '#414833',
                backgroundColor: 'rgba(65, 72, 51, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Validation Loss',
                data: [1.3, 1.2, 1.1, 1.0, 0.95, 0.85, 0.8, 0.75, 0.7, 0.65, 0.62, 0.6, 0.58],
                borderColor: '#737A5D',
                backgroundColor: 'rgba(115, 122, 93, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },

        // Price Trend Chart Data
        priceTrendData: {
            labels: ['1987', '1990', '1993', '1996', '1999', '2002', '2005', '2008', '2011', '2014', '2017', '2018'],
            datasets: [{
                label: 'Brent Crude Oil Price',
                data: [15, 18, 22, 25, 28, 32, 38, 55, 65, 75, 85, 90],
                borderColor: '#414833',
                backgroundColor: 'rgba(65, 72, 51, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 3
            }]
        },

        // City Price Chart Data
        cityPriceData: {
            labels: ['Barcelona', 'Madrid', 'Valencia', 'Malaga', 'Girona', 'Mallorca', 'Sevilla', 'Menorca'],
            datasets: [{
                label: 'Average Price (€)',
                data: [1295, 938, 794, 817, 1229, 1713, 1046, 1647],
                backgroundColor: ['#414833', '#737A5D', '#A4AC86', '#CCBFA3', '#EBE3D2', '#A4AC86', '#737A5D', '#414833'],
                borderColor: '#414833',
                borderWidth: 1
            }]
        },

        // Room Type Comparison Chart Data
        roomTypeData: {
            labels: ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room'],
            datasets: [{
                label: 'Average Price (€)',
                data: [1295, 455, 373, 1444],
                backgroundColor: ['#414833', '#737A5D', '#A4AC86', '#CCBFA3'],
                borderColor: '#414833',
                borderWidth: 1
            }]
        },

        // Price Trend Analysis Chart Data
        priceTrendAnalysisData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Price Trend',
                data: [45, 48, 52, 49, 55, 58, 60, 57, 54, 52, 49, 47],
                borderColor: '#414833',
                backgroundColor: 'rgba(65, 72, 51, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        }
    };

    // Initialize charts with error handling
    try {
        // LSTM Charts
        if (document.getElementById('predictionChart')) {
            createChart('predictionChart', 'line', sampleData.predictionData, { title: 'Price Prediction vs Actual' });
        }

        if (document.getElementById('lossChart')) {
            createChart('lossChart', 'line', sampleData.lossData, { title: 'Model Training Performance' });
        }

        if (document.getElementById('priceTrendChart')) {
            createChart('priceTrendChart', 'line', sampleData.priceTrendData, { title: 'Crude Oil Price Trend (1987-2018)' });
        }

        // Marketing Analysis Charts
        if (document.getElementById('cityPriceChart')) {
            createChart('cityPriceChart', 'bar', sampleData.cityPriceData, { title: 'Average Prices by City' });
        }

        if (document.getElementById('roomTypeChart')) {
            createChart('roomTypeChart', 'bar', sampleData.roomTypeData, { title: 'Price Comparison by Room Type' });
        }

        if (document.getElementById('priceTrendAnalysisChart')) {
            createChart('priceTrendAnalysisChart', 'line', sampleData.priceTrendAnalysisData, { title: 'Price Trend Analysis' });
        }
    } catch (error) {
        console.error('Error initializing charts:', error);
        // Fallback: Show a message if charts fail to load
        const chartContainers = document.querySelectorAll('.visualization-placeholder');
        chartContainers.forEach(container => {
            const fallback = document.createElement('p');
            fallback.textContent = 'Interactive charts would appear here when the page loads properly.';
            fallback.style.color = '#737A5D';
            fallback.style.fontStyle = 'italic';
            container.appendChild(fallback);
        });
    }
});