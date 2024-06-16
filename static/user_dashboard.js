console.log('Hey');

async function fetchData() {
  const response = await fetch('/pie');
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
                backgroundColor: ['#FF6384', '#36A2EB'],
                hoverBackgroundColor: ['#FF6384', '#36A2EB']
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

document.addEventListener('DOMContentLoaded', createChart);