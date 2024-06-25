async function fetchData() {
    const username = document.getElementById('username').value;
    const response = await fetch(`/pie/${username}`);
    const data = await response.json();
    return data;
}

async function createChart() {
    const data = await fetchData();
    const ctx = document.getElementById('myPieChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Broken Cameras',
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
                    position: 'top',
                },
                tooltip: {
                    enabled: true
                }
                }
            }
        });
}

async function fetchUserList() {
    const response = await fetch('/getuserlist', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        redirect: 'follow'
    });
    const data = await response.json();
    return data;
}

async function populateUserList() {
    const users = await fetchUserList();
    const userList = document.getElementById('user-list');
    users.forEach(user => {
        const userLink = document.createElement('a');
        // userLink.href = `/user_dashboard/${user.username}`;
        userLink.textContent = user.username;
        userLink.style.cursor = 'pointer';
        userLink.addEventListener('click', () => {
            createChartUser(user.username);
        });
        userList.appendChild(userLink);
    });
}

let newChartInstance;

async function createChartUser(username) {
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
                label: 'Broken Cameras',
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
                    position: 'top',
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });
}





document.addEventListener('DOMContentLoaded', () => {
    createChart();
    populateUserList();
});