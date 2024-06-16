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
    console.log(users);
    const userList = document.getElementById('user-list');
    users.forEach(user => {
        console.log(user)
        const userLink = document.createElement('a');
        userLink.href = `/user_dashboard/${user.username}`;
        userLink.textContent = user.username;
        userList.appendChild(userLink);
    });
}



document.addEventListener('DOMContentLoaded', () => {
    createChart();
    populateUserList();
});