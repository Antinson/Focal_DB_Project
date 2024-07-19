document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(registerForm);
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
        role: formData.get('roles'),
        country: formData.get('country')
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message == 'Creation successful') {
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }
        document.getElementById('errorMessage').innerText = data.message;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});