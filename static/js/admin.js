document.addEventListener('DOMContentLoaded', function() {
    const subjectCanvas = document.getElementById('subjectChart');
    const subjectLabels = JSON.parse(subjectCanvas.dataset.labels || '["No Data"]');
    const subjectCounts = JSON.parse(subjectCanvas.dataset.counts || '[0]');

    const subjectCtx = subjectCanvas.getContext('2d');
    new Chart(subjectCtx, {
        type: 'pie',
        data: {
            labels: subjectLabels,
            datasets: [{
                data: subjectCounts,
                backgroundColor: [
                    'rgba(76, 81, 191, 0.8)',  // #4C51BF
                    'rgba(99, 179, 237, 0.8)', // #63B3ED
                    'rgba(72, 187, 120, 0.8)', // #48BB78
                    'rgba(0, 181, 216, 0.8)',  // #00B5D8
                    'rgba(237, 137, 54, 0.8)', // #ED8936
                    'rgba(246, 173, 85, 0.8)'  // #F6AD55
                ],
                borderColor: 'rgba(255, 255, 255, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#2D3748',
                        font: {
                            size: 14
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(45, 55, 72, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            }
        }
    });

    const quizCanvas = document.getElementById('quizAttemptsChart');
    const quizLabels = JSON.parse(quizCanvas.dataset.labels || '["No Data"]');
    const quizCounts = JSON.parse(quizCanvas.dataset.counts || '[0]');

    const quizCtx = quizCanvas.getContext('2d');
    new Chart(quizCtx, {
        type: 'bar',
        data: {
            labels: quizLabels,
            datasets: [{
                label: 'Quiz Attempts',
                data: quizCounts,
                backgroundColor: 'rgba(76, 81, 191, 0.7)', // #4C51BF
                borderColor: 'rgba(76, 81, 191, 1)',
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        color: '#2D3748'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#2D3748'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#2D3748'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(45, 55, 72, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            }
        }
    });
});