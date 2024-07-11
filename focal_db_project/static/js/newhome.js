



const createChart = () => {
    fetch()
}

const updateTable = (filters) => {
    const { country, user, cameraType, cameraStatus } = filters;

    const params = new URLSearchParams({
        country: country || '',
        user: user || '',
        cameraType: cameraType || '',
        cameraStatus: cameraStatus || ''
    });

    fetch(`/api/get-cameras-dash?${params.toString()}`)
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#table-body tbody');
        tableBody.innerHTML = '';

        data.forEach(camera => {
            const row = document.createElement('tr');
            row.innerHTML = `
                        <td class="border px-4 py-2">${camera.camera_name}</td>
                        <td class="border px-4 py-2">${camera.camera_type}</td>
                        <td class="border px-4 py-2">${camera.camera_status}</td>
                        <td class="border px-4 py-2">${camera.camera_country}</td>
                        <td class="border px-4 py-2">${camera.camera_storage}</td>
                        `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching data:', error));
}

const updateFilters = (filters) => {
    const { country, user, cameraType, cameraStatus } = filters;

    const params = new URLSearchParams({
        country: country || '',
        user: user || '',
        cameraType: cameraType || '',
        cameraStatus: cameraStatus || ''
    });

    fetch(`/api/get-filtered-options?${params.toString()}`)
    .then(response => response.json())
    .then(data => {
        updateFilterOptions(userFilter, data.users);
        updateFilterOptions(cameraTypeFilter, data.camera_types);
        updateFilterOptions(cameraStatusFilter, data.camera_status);
    })
    .catch(error => console.error('Error fetching filter options:', error));
}

const updateFilterOptions = (filterElement, options) => {
    
    filterElement.innerHTML = '<option value="">Dropdown</option>';
    
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option.value;
        opt.textContent = option.text;
        filterElement.appendChild(opt);
    });
}




document.addEventListener('DOMContentLoaded', () => {

    const countryFilter = document.getElementById('country-filter');
    const userFilter = document.getElementById('user-filter');
    const cameraTypeFilter = document.getElementById('camera-type-filter');
    const cameraStatusFilter = document.getElementById('camera-status-filter');

    const filters = [countryFilter, userFilter, cameraTypeFilter, cameraStatusFilter];
    updateTable(filters);

    filters.forEach(filter => {
        filter.addEventListener('change', () => {
            const selectedFilters = {
                country: countryFilter.value,
                user: userFilter.value,
                cameraType: cameraTypeFilter.value,
                cameraStatus: cameraStatusFilter.value
            };
            updateFilters(selectedFilters);
            updateTable(selectedFilters);
    });
    });
});