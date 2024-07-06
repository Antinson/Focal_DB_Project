let mainChart;
let newChartInstance;


export async function createChartUser(username) {
    const response = await fetch(`/pie/${username}`);
    const data = await response.json();
    const ctx = document.getElementById('newChart').getContext('2d');
    const userPreview = document.getElementById('user_fill');
    userPreview.textContent = `Preview for ${username}`;
    userPreview.addEventListener('click', () => {
        // Go to /user_dashboard/username
        window.location.href = `/user_dashboard/${username}`;
    });
    // Add hover pointer to the user preview
    userPreview.style.cursor = 'pointer';

    if (newChartInstance) {
        newChartInstance.destroy();
    }

    newChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Cameras',
                data: data.values,
                backgroundColor: ['#36A2EB', '#FF6384'],
                hoverBackgroundColor: ['#36A2EB', '#FF6384'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false // Hide the legend,
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });
}

export async function createChart() {
    const data = await fetchData();
    const ctx = document.getElementById('myPieChart').getContext('2d');

    if (mainChart) {
        mainChart.destroy();
    }

    mainChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Cameras',
                data: data.values,
                backgroundColor: ['#36A2EB', '#FF6384'],
                hoverBackgroundColor: ['#36A2EB', '#FF6384'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false // Hide the legend
                },
                tooltip: {
                    enabled: true
                },
                datalabels: {
                    anchor: 'middle',
                    align: 'end',
                    color: '#000',
                    font: {
                        weight: 'bold'
                    },
                    formatter: function(value, context) {
                        return value; 
                    }
                }
                }
            }
        });
}

async function fetchData() {
    const username = document.getElementById('username').value;
    const response = await fetch(`/pie/${username}`);
    const data = await response.json();
    return data;
}