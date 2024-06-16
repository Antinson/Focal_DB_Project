async function fetchData() {
    const username = document.getElementById('username').value;
    const response = await fetch(`/pie/${username}`);
    const data = await response.json();
    console.log('Here');
    return data;
}

async function createChart() {
    const data = await fetchData();
    const ctx = document.getElementById('myPieChart').getContext('2d');
    console.log('Here')

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Camera Status',
                data: data.values,
                backgroundColor: ['#36A2EB', '#FF6384'],
                hoverBackgroundColor: ['#36A2EB', '#FF6384']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    enabled: true
                }
                }
            }
        }
    )
}

document.addEventListener('DOMContentLoaded', () => {
    createChart();
});