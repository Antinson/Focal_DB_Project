document.addEventListener('DOMContentLoaded', function() {
    const cameraInput = document.getElementById('cameraid');

    cameraInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            // Prevent the default action (form submission)
            event.preventDefault();

            // Get the input value
            const cameraId = cameraInput.value;

            // Create the POST request
            fetch('api/addbrokencamera', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cameraid: cameraId })
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    });
});
