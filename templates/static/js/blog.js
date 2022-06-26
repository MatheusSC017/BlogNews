const state = ['none', 'block']

function popupForm(form, show) {
    document.getElementById(form).style.display = state[show]
    document.getElementById('popup').style.display = state[show]
}

function commentField(pk) {
    comment = document.querySelector('#comment-' + pk + ' > p').innerText
    document.querySelector('#update-comment-form textarea').value = comment
}

function albumFields(pk) {
    title = document.querySelector('#album-' + pk + '> td:nth-child(2)').innerText
    document.querySelector('#update-album-form input[type="text"]').value = title

    published = document.querySelector('#album-' + pk + '> td:nth-child(3)').innerText
    published_field = document.querySelector('#update-album-form input[type="checkbox"]')
    published_field.checked = false
    if (published == 'Sim')
        published_field.checked = true
}

function imageFields(pk) {
    title = document.querySelector('#image-' + pk + ' img').getAttribute('title')
    document.getElementById('title-image-id').value = title
}

function pkField(form, pk) {
    document.querySelector('#' + form + ' input[name="primary-key"]').value = pk
}

function checkboxSelection(pk) {
    visible_state = ['visible', 'hidden']
    checkbox_element = document.getElementById('check-delete-' + pk)
    checkbox_state = checkbox_element.checked
    checkbox_element.checked = !checkbox_state
    document.getElementById('checked-icon-delete-' + pk).style.visibility = visible_state[Number(checkbox_state)]
    return false
}

function confirmAction() {
    return confirm('Deseja apagar os itens selecionados?')
}