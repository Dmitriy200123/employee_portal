let selectDepartment = document.querySelector('.form_department .department')
selectDepartment.addEventListener('change', getPosition)
getPosition()


function getPosition() {
    let selectedValue = selectDepartment.options[selectDepartment.selectedIndex].value;
    responsePositions(selectedValue).then(data => {
        let selectPosition = document.querySelector('.form_position .position')
        removeOptions(selectPosition)

        if (data != null)
            addPositions(selectPosition, data)
    })
}

function responsePositions(value) {
    return fetch(`/positions/${value}/`, {method: 'GET'}).then(response => {
        if (response.ok) {
            return response.json()
        }
        if (response.status === 404) {
            return null
        } else {
            return Promise.reject(response)
        }
    })
}

function addPositions(selectPosition, positions) {
    selectPosition.appendChild(createOption({'id': null, 'name': 'Выберите должность'}))

    for (let position of positions) {
        selectPosition.appendChild(createOption(position));
    }
}

function createOption(position) {
    let option = document.createElement('option');
    option.innerHTML = position['name'];

    if (position['id'] != null)
        option.value = position['id'];

    return option
}

function removeOptions(selectElement) {
    for (let i = selectElement.options.length - 1; i >= 0; i--) {
        selectElement.remove(i);
    }
}