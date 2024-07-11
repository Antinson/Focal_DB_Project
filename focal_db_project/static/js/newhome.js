document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');

    const countryFilter = document.getElementById('country-filter');
    const userFilter = document.getElementById('user-filter');
    const cameraTypeFilter = document.getElementById('camera-type-filter');
    const cameraStatusFilter = document.getElementById('camera-status-filter');

    // Ensure the elements are found
    if (!countryFilter || !userFilter || !cameraTypeFilter || !cameraStatusFilter) {
        console.error('One or more filter elements are not found in the DOM');
        console.error('countryFilter:', countryFilter);
        console.error('userFilter:', userFilter);
        console.error('cameraTypeFilter:', cameraTypeFilter);
        console.error('cameraStatusFilter:', cameraStatusFilter);
        return;
    }

    const filters = [countryFilter, userFilter, cameraTypeFilter, cameraStatusFilter];
    
    // Function to get the selected filters
    const getSelectedFilters = () => {
        return {
            country: countryFilter.value,
            user: userFilter.value,
            cameraType: cameraTypeFilter.value,
            cameraStatus: cameraStatusFilter.value
        };
    };

    // Initialize the filters and table on page load
    const initPage = () => {
        console.log('Fetching initial filter options');
        fetch('/api/get-filtered-options')
        .then(response => response.json())
        .then(data => {
            console.log('Initial filter options fetched:', data);
            updateFilterOptions(countryFilter, data.countries);
            updateFilterOptions(userFilter, data.users);
            updateFilterOptions(cameraTypeFilter, data.camera_types);
            updateFilterOptions(cameraStatusFilter, data.camera_statuses);
            
            updateTable(getSelectedFilters());
        })
        .catch(error => console.error('Error fetching initial filter options:', error));
    };

    // Add event listeners to each filter
    filters.forEach(filter => {
        filter.addEventListener('change', () => {
            console.log('Filter changed:', filter.id);
            const selectedFilters = getSelectedFilters();
            console.log('Selected filters:', selectedFilters);
            updateFilters(selectedFilters);
            updateTable(selectedFilters);
        });
    });

    // Call initPage to initialize filters and table on page load
    initPage();
});

const updateTable = (filters) => {
    console.log('Updating table with filters:', filters);
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
        console.log('Table data fetched:', data);
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
    .catch(error => console.error('Error fetching table data:', error));
};

const updateFilters = (filters) => {
    console.log('Updating filters with:', filters);
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
        console.log('Filter options fetched:', data);
        updateFilterOptions(document.getElementById('user-filter'), data.users);
        updateFilterOptions(document.getElementById('camera-type-filter'), data.camera_types);
        updateFilterOptions(document.getElementById('camera-status-filter'), data.camera_statuses);
    })
    .catch(error => console.error('Error fetching filter options:', error));
};

const updateFilterOptions = (filterElement, options) => {
    if (!filterElement) {
        console.error('Filter element not found');
        return;
    }

    const selectedValue = filterElement.value;


    // Handle cases where options might be undefined or null
    options = options || [];

    filterElement.innerHTML = '';

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Dropdown';
    filterElement.appendChild(defaultOption);

    
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        filterElement.appendChild(opt);
    });

    filterElement.value = selectedValue;
};
