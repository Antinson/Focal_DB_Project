const submit = document.getElementById('download');
const selectValue = document.getElementById('formats');
const username = document.getElementById('username').value;

submit.addEventListener('click', () => {
    let selectedValue = selectValue.value;
    sendForm(selectedValue)
});

const sendForm = (selectedValue) => {
    fetch('/api/download-usertable', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({filetype: selectedValue, user: username})
    })
    .then(response => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition ? contentDisposition.split('filename=')[1].replace(/\"/g, '') : 'default_filename';
        return response.blob().then(blob => {
            return {blob, filename}
        })

    })
    .then(({ blob, filename }) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename.replace(/\"/g, ''); // Remove any potential quotes around the filename
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    })
    .catch(error => console.error('Error downloading the file:', error));
}

const getCameraCountsByType = (username) => {
    fetch(`/api/get-camera-counts-by-type/${username}`)
    .then(response => response.json())
    .then(data => {
        const summaryContainer = document.getElementById('summary_container');
        summaryContainer.innerHTML = '';

        for (const [type, count] of Object.entries(data)) {
            const container = document.createElement('div');
            const div = document.createElement('div');
            const div2 = document.createElement('div');
            const displayType = type == 'None' ? 'Unknown' : type;

            div.textContent = `${displayType}`;
            div2.textContent = `${count}`

            // Append the new div to the container
            container.appendChild(div)
            container.appendChild(div2);
            summaryContainer.appendChild(container);
        }
    })
    .catch(error => console.error('Error:', error));
}

const camera_table = document.getElementById("camera_table");
let currentPage = 1;
const perPage = 20;

const fetchCameras = (username, cameraType, status, page = 1, perPage = 5) => {
    let url = `/api/get-camera-user/${username}?page=${page}&per_page=${perPage}`;
    if (cameraType) {
        url += `&camera_type=${cameraType}`;
    }
    if (status) {
        url += `&status=${status.toLowerCase()}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const cameras = data.data;
            const total = data.total;
            const totalPages = Math.ceil(total / perPage);

            camera_table.innerHTML = '';
            const table = document.createElement("table");
            table.classList.add("table-auto", "w-full", "bg-gray-100", "rounded-lg");
            const thead = document.createElement("thead");
            thead.innerHTML = `
                <tr>
                    <th class="px-4 py-2">Camera Name</th>
                    <th class="px-4 py-2">Status</th>
                    <th class="px-4 py-2">Type</th>
                    <th class="px-4 py-2">Edit</th>
                </tr>
            `;
            table.appendChild(thead);

            const tbody = document.createElement("tbody");
            cameras.forEach(camera => {
                if (camera.camera_type == null) {
                    camera.camera_type = "Unknown";
                }
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td class="border px-4 py-2">${camera.camera_name}</td>
                    <td class="border px-4 py-2">${camera.camera_status}</td>
                    <td class="border px-4 py-2">${camera.camera_type}</td>
                    <td class="border px-4 py-2"><button class="edit-button" data-camera-name="${camera.camera_name}">Edit</button></td>
                `;
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            camera_table.appendChild(table);

            document.querySelectorAll('.edit-button').forEach(button => {
                button.addEventListener('click', event => {
                    const cameraName = event.target.getAttribute('data-camera-name');
                    localStorage.setItem('lastLocation', window.location.href);
                    window.location.href = `/editcamera/${cameraName}`;
                });
            });

            // Create pagination controls
            const paginationControls = document.getElementById('pagination-controls');
            paginationControls.innerHTML = '';
            for (let i = 1; i <= totalPages; i++) {
                const pageButton = document.createElement('button');
                pageButton.textContent = i;
                pageButton.classList.add('px-2', 'py-1', 'm-1', 'border', 'rounded');
                if (i === page) {
                    pageButton.classList.add('bg-blue-500', 'text-white');
                }
                pageButton.addEventListener('click', () => {
                    currentPage = i;
                    fetchCameras(username, cameraType, status, currentPage, perPage);
                });
                paginationControls.appendChild(pageButton);
            }
        });
}

document.getElementById('camera_type_filter').addEventListener('change', () => {
    const cameraType = document.getElementById('camera_type_filter').value;
    const status = document.getElementById('status_filter').value;
    fetchCameras(username, cameraType, status, currentPage, perPage);
});

document.getElementById('status_filter').addEventListener('change', () => {
    const cameraType = document.getElementById('camera_type_filter').value;
    const status = document.getElementById('status_filter').value;
    fetchCameras(username, cameraType, status, currentPage, perPage);
});

const createSelectionValues = () => {
    const selectOptions = document.getElementById('camera_type_filter');

    fetch(`/api/get-camera-counts-by-type/${username}`)
    .then(response => response.json())
    .then(data => {
        for (const [type, count] of Object.entries(data)) {
            const displayType = type == 'None' ? 'Unknown' : type;
            const newOption = document.createElement('option')
            newOption.value = `${displayType}`;
            newOption.text = `${displayType}`;
            selectOptions.appendChild(newOption);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Initial fetch without filters
fetchCameras(username, '', '', currentPage, perPage);
getCameraCountsByType(username);
createSelectionValues();