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
    if (published == 'Sim') {
        published_field.checked = true
    }
}

function imageFields(pk) {
    title = document.querySelector('#image-' + pk + ' img').getAttribute('title')
    document.querySelector('#title-image-id').value = title
}

function pkField(form, pk) {
    document.querySelector('#' + form + ' input[name="primary-key"]').value = pk
}
