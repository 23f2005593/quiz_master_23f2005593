document.addEventListener('DOMContentLoaded', function() {
    const chartData = document.getElementById('chartData');
    
    const getJsonData = (attr) => {
        try {
            return JSON.parse(chartData.getAttribute(attr) || '[]');
        } catch (e) {
            console.error('Error parsing JSON data:', e);
            return [];
        }
    };
    
    const subjectLabels = getJsonData('data-subject-labels');
    const subjectScores = getJsonData('data-subject-scores');
    const subjectAttempts = getJsonData('data-subject-attempts');
    const monthLabels = getJsonData('data-month-labels');
    const monthCounts = getJsonData('data-month-counts');
    const trendDates = getJsonData('data-trend-dates');
    const trendScores = getJsonData('data-trend-scores');
    
    // Common chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            }
        }
    };
    
    if (subjectLabels.length > 0 && document.getElementById('subjectChart')) {
        const subjectCtx = document.getElementById('subjectChart').getContext('2d');
        const subjectChart = new Chart(subjectCtx, {
            type: 'bar',
            data: {
                labels: subjectLabels,
                datasets: [
                    {
                        label: 'Average Score (%)',
                        data: subjectScores,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Attempts',
                        data: subjectAttempts,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        type: 'line',
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Average Score (%)'
                        },
                        max: 100
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Number of Attempts'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
    
    if (document.getElementById('monthlyChart')) {
        const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
        const monthlyChart = new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: monthLabels,
                datasets: [{
                    label: 'Quizzes Attempted',
                    data: monthCounts,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Quizzes'
                        }
                    }
                }
            }
        });
    }
    
    if (trendScores.length > 0 && document.getElementById('trendChart')) {
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        const trendChart = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendDates,
                datasets: [{
                    label: 'Score (%)',
                    data: trendScores,
                    fill: {
                        target: 'origin',
                        above: 'rgba(75, 192, 192, 0.2)'
                    },
                    borderColor: 'rgba(75, 192, 192, 1)',
                    tension: 0.3,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Score (%)'
                        }
                    }
                },
                elements: {
                    line: {
                        borderWidth: 2
                    }
                }
            }
        });
    }
});