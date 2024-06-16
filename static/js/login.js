document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    console.log(JSON.stringify({ username: username, password: password }))

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Login successful') {
            window.location.href = '/dashboard';
        } else {
            document.getElementById('errorMessage').innerText = data.message;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});