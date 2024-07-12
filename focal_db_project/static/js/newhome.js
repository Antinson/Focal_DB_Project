let savedStates = {
    country: [],
    user: [],
    cameraType: [],
    cameraStatus: []
};

// Function definitions
function showCheckboxes(checkboxesId) {
    closeAllCheckboxes();
    var checkboxes = document.getElementById(checkboxesId);
    checkboxes.style.display = 'block';
}

function closeAllCheckboxes() {
    document.querySelectorAll('.checkboxes').forEach(checkboxContainer => {
        checkboxContainer.style.display = 'none';
        updateSelectBoxLabel(checkboxContainer.id);
    });
}

function selectAll(checkboxesId, selectAllCheckbox) {
    var checkboxes = document.querySelectorAll(`#${checkboxesId} .checkbox`);
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
    updateSelectAllState(checkboxesId);
    updateSelectBoxLabel(checkboxesId);
}

function getSelectedCheckboxes(checkboxesId) {
    const selectedCheckboxes = [];
    const checkboxes = document.querySelectorAll(`#${checkboxesId} .checkbox`);
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedCheckboxes.push(checkbox.value);
        }
    });
    return selectedCheckboxes;
}

function updateFilterOptions(checkboxesId, options) {
    if (!options) return;
    const checkboxesContainer = document.getElementById(checkboxesId);
    if (!checkboxesContainer) return;

    const filterType = checkboxesId.replace('-checkboxes', '');
    console.log(`Updating filter options for ${filterType}:`, options);

    // Preserve the previously selected values
    const selectedValues = savedStates[filterType] || [];
    console.log(`Previously selected values for ${filterType}:`, selectedValues);

    checkboxesContainer.innerHTML = `
        <label for="${checkboxesId}-select-all">
            <input type="checkbox" id="${checkboxesId}-select-all"> Select All
        </label>
    `;

    options.forEach(option => {
        const opt = document.createElement('label');
        opt.innerHTML = `<input type="checkbox" class="checkbox" value="${option}"> ${option}`;
        checkboxesContainer.appendChild(opt);
    });

    // Restore the previously selected values
    document.querySelectorAll(`#${checkboxesId} .checkbox`).forEach(checkbox => {
        if (selectedValues.includes(checkbox.value)) {
            checkbox.checked = true;
        }
        checkbox.addEventListener('change', () => {
            updateSelectAllState(checkboxesId);
            updateSelectBoxLabel(checkboxesId);
            // Save the current selected values to savedStates
            savedStates[filterType] = getSelectedCheckboxes(checkboxesId);
            console.log(`Updated savedStates for ${filterType}:`, savedStates[filterType]);
        });
    });

    // Set event listener for select all checkbox
    document.getElementById(`${checkboxesId}-select-all`).addEventListener('click', (event) => {
        selectAll(checkboxesId, event.target);
        // Save the current selected values to savedStates
        savedStates[filterType] = getSelectedCheckboxes(checkboxesId);
        console.log(`Updated savedStates for ${filterType}:`, savedStates[filterType]);
    });

    updateSelectAllState(checkboxesId);
    updateSelectBoxLabel(checkboxesId);
}

function updateSelectAllState(checkboxesId) {
    const checkboxes = document.querySelectorAll(`#${checkboxesId} .checkbox`);
    const selectAllCheckbox = document.querySelector(`#${checkboxesId} #${checkboxesId}-select-all`);
    const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
    selectAllCheckbox.checked = allChecked;
}

function updateSelectBoxLabel(checkboxesId) {
    const selectedValues = getSelectedCheckboxes(checkboxesId);
    const filterType = checkboxesId.replace('-checkboxes', '');
    console.log(`Selected values for ${filterType}:`, selectedValues);

    const selectBox = document.querySelector(`[data-checkboxes-id="${checkboxesId}"] select`);

    if (selectedValues.length === 0) {
        selectBox.innerHTML = '<option value="">Dropdown</option>';
    } else if (selectedValues.length === 1) {
        selectBox.innerHTML = `<option value="${selectedValues[0]}">${selectedValues[0]}</option>`;
    } else if (selectedValues.length === document.querySelectorAll(`#${checkboxesId} .checkbox`).length) {
        selectBox.innerHTML = '<option value="">(ALL)</option>';
    } else {
        selectBox.innerHTML = '<option value="">(Multiple Selections)</option>';
    }
}

function updateTable(filters) {
    const { country, user, cameraType, cameraStatus } = filters;

    // Save the current states
    savedStates.country = country;
    savedStates.user = user;
    savedStates.cameraType = cameraType;
    savedStates.cameraStatus = cameraStatus;

    fetch('/api/get-cameras-dash', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#table-body tbody');
        tableBody.innerHTML = '';

        const cameras = data.cameras;
        const camera_names = cameras.map(camera => camera.camera_name);
        const counts = data.counts;

        cameras.forEach(camera => {
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
        updateCounts(counts);
        getTimeStamps(camera_names, counts.total);

    })
    .catch(error => console.error('Error fetching table data:', error));
}

function updateFilters(filters) {
    fetch('/api/get-filtered-options', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => {
        updateFilterOptions('country-checkboxes', data.countries);
        updateFilterOptions('user-checkboxes', data.users);
        updateFilterOptions('camera-type-checkboxes', data.camera_types);
        updateFilterOptions('camera-status-checkboxes', data.camera_statuses);
    })
    .catch(error => console.error('Error fetching filter options:', error));
}

function updateCounts(counts) {
    if (!counts) {
        console.error('Counts data not provided');
        return;
    }

    document.getElementById('total-camera-num').textContent = `${counts.total}`;
    document.getElementById('broken-camera-num').textContent = `${counts.broken}`;
    document.getElementById('working-camera-num').textContent = `${counts.working}`;
}

// DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', () => {
    const filters = [
        { id: 'country-filter-container', checkboxesId: 'country-checkboxes' },
        { id: 'user-filter-container', checkboxesId: 'user-checkboxes' },
        { id: 'camera-type-filter-container', checkboxesId: 'camera-type-checkboxes' },
        { id: 'camera-status-filter-container', checkboxesId: 'camera-status-checkboxes' }
    ];

    const initPage = () => {
        fetch('/api/get-filtered-options', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            updateFilterOptions('country-checkboxes', data.countries);
            updateFilterOptions('user-checkboxes', data.users);
            updateFilterOptions('camera-type-checkboxes', data.camera_types);
            updateFilterOptions('camera-status-checkboxes', data.camera_statuses);
            updateTable(getSelectedFilters());
        })
        .catch(error => console.error('Error fetching initial filter options:', error));
    };

    const getSelectedFilters = () => {
        const selectedCountries = getSelectedCheckboxes('country-checkboxes');
        const selectedUsers = getSelectedCheckboxes('user-checkboxes');
        const selectedCameraTypes = getSelectedCheckboxes('camera-type-checkboxes');
        const selectedCameraStatuses = getSelectedCheckboxes('camera-status-checkboxes');

        return {
            country: selectedCountries,
            user: selectedUsers,
            cameraType: selectedCameraTypes,
            cameraStatus: selectedCameraStatuses
        };
    };

    filters.forEach(filter => {
        const filterElement = document.getElementById(filter.id);
        if (filterElement) {
            filterElement.addEventListener('change', () => {
                const selectedFilters = getSelectedFilters();
                updateFilters(selectedFilters);
                updateTable(selectedFilters);
            });
        }
    });

    // Set click event listeners for each select box to show checkboxes
    document.querySelectorAll('.select-box').forEach(selectBox => {
        selectBox.addEventListener('click', (event) => {
            event.stopPropagation();
            showCheckboxes(selectBox.getAttribute('data-checkboxes-id'));
        });
    });

    initPage();
});

// Add event listener to close all checkboxes when clicking outside
document.addEventListener('click', (event) => {
    if (!event.target.closest('.select-box') && !event.target.closest('.checkboxes')) {
        closeAllCheckboxes();
    }
}, true);

const getTimeStamps = (cameraNames, count) => {
    if (!cameraNames || cameraNames.length === 0) return;
    console.log('Start of getTimeStamps');

    fetch('/api/get-timestamps', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ camera_names: cameraNames })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Timestamps and statuses:', data);
        processChartData(data, count);
    })
    .catch(error => {
        console.error('Error fetching timestamps:', error);
    });
}

const processChartData = (data, count) => {
    const initialWorkingCameras = count;  // Initial total working cameras
    const workingData = {};
    const dateRange = [];

    console.log('Start of ProcessChartData');

    // Create a date range array for the last 14 days
    for (let i = 0; i < 14; i++) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateString = date.toISOString().split('T')[0];
        dateRange.unshift(dateString);
        workingData[dateString] = 0;
    }

    // Process data to count broken cameras each day
    data.forEach(entry => {
        const date = entry.timestamp.split('T')[0];
        if (date in workingData && entry.status === 'broken') {
            workingData[date]++;
        }
    });

    // Calculate the cumulative number of working cameras each day
    let cumulativeWorking = initialWorkingCameras;
    const cumulativeWorkingData = dateRange.map(date => {
        cumulativeWorking -= workingData[date];
        return cumulativeWorking;
    });
    console.log('End of ProcessChartData');

    createChart(dateRange, cumulativeWorkingData);
}

const createChart = (labels, workingData) => {
    const ctx = document.createElement('canvas');
    ctx.width = 800;  // Set the width of the canvas
    ctx.height = 400; // Set the height of the canvas

    const mainChartDiv = document.getElementById('main-chart');
    mainChartDiv.innerHTML = '';  // Clear any existing content
    mainChartDiv.appendChild(ctx);  // Append the new canvas element
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Working Cameras',
                    data: workingData,
                    borderColor: 'rgba(40, 153, 109, 0.9)',
                    backgroundColor: 'rgba(48, 185, 132, 0.1)', // Light green background for the line
                    tension: 0.1, // Smooth the line
                    pointRadius: 0, // Hide points
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 14
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Working Cameras'
                    },
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1, // Ensure y-axis has whole numbers
                        callback: function(value) {
                            return Number.isInteger(value) ? value : null;
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false // Hide legend
                },
                tooltip: {
                    enabled: true // Enable tooltips
                },
                title: {
                    display: true,
                    text: 'Working Cameras Over Time'
                }
            },
            responsive: true,
            maintainAspectRatio: false // Allow the chart to take the size of its container
        }
    });
}
