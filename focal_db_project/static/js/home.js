import { createChart, createChartUser } from './graphs.js'

const broken = document.getElementById('camera-list');
        
fetch('/api/createnotifications').then(response => response.json()).then(data => {
});


function fetchStockLevels() {
    fetch('/api/getnotifications')
        .then(response => response.json())
        .then(data => {
            
            broken.innerHTML = '';
            
            data.forEach(notification =>{
                const userDiv = document.createElement('div');
                userDiv.textContent = notification.message;
                userDiv.style.cursor = 'pointer';
                userDiv.addEventListener('click', () => {
                    deleteNotification(notification.id);
                })
                broken.appendChild(userDiv);
                console.log('Success');
            })
        });
}

function deleteNotification(id) {
    fetch('/api/deletenotification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id: id}),
    })
    .then(response => response.json())
    .then(data => {
        fetchStockLevels();
    });
}




document.addEventListener('DOMContentLoaded', () => {
    fetchStockLevels();
    createChart();
    Chart.register(ChartDataLabels);
});