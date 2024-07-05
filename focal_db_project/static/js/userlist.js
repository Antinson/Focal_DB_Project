import { createChart, createChartUser } from './graphs.js'


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


document.addEventListener('DOMContentLoaded', () => {
    createChart();
    Chart.register(ChartDataLabels);
    populateUserList();
});

