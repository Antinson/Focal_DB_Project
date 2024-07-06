document.addEventListener('DOMContentLoaded', function() {
    const cameraInput = document.getElementById('cameraid');
    const toast = document.getElementById('toast');

    cameraInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            // Prevent the default action (form submission)
            event.preventDefault();

            // Get the input value
            const cameraId = cameraInput.value;
            console.log('Captured value:', cameraId);

            // Clear the input field immediately
            cameraInput.value = 'test';
            console.log('Input value after clearing:', cameraInput.value);

            // Create the POST request
            fetch('api/addcamera', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        cameraid: cameraId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    showToast(data.message);
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                    showToast('An error occurred while adding the camera.');
                });
        }
    });

    function showToast(message) {
        toast.textContent = message;
        toast.className = "show";
        setTimeout(() => {
            toast.className = toast.className.replace("show", "");
        }, 3000);
    }
});
