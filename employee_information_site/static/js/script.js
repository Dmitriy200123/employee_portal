let selectDepartment = document.querySelector('.form_department .department')
selectDepartment.addEventListener('change', getPosition)
getPosition()


function getPosition() {
    let selectedValue = selectDepartment.value
    responsePositions(selectedValue).then(data => {
        let selectPosition = document.querySelector('.form_position .position')
        selectPosition.containsOption = containsOption
        let positionValue = selectPosition.value

        removeOptions(selectPosition)

        if (data != null) {
            addPositions(selectPosition, data)
            selectOption(selectPosition, positionValue)
        }
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
    let defaultOption = {'id': '', 'name': 'Выберите должность'}
    selectPosition.appendChild(createOption(defaultOption))

    for (let position of positions) {
        selectPosition.appendChild(createOption(position))
    }
}

function selectOption(selectPosition, positionValue) {
    if (selectPosition.containsOption(positionValue))
        selectPosition.value = positionValue
    else
        selectPosition.value = ''
}

function containsOption(value) {
    for (let i = 0, l = this.options.length; i < l; i++) {
        if (this.options[i].value === value)
            return true
    }

    return false
}

function createOption(position) {
    let option = document.createElement('option')
    option.innerHTML = position['name']
    option.value = position['id']

    return option
}

function removeOptions(selectElement) {
    for (let i = selectElement.options.length - 1; i >= 0; i--) {
        selectElement.remove(i)
    }
}