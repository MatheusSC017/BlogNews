const state = ['none', 'block']

function popupForm(form, show) {
    document.getElementById(form).style.display = state[show]
    document.getElementById('popup').style.display = state[show]
}

function commentField(pk) {
    comment = document.querySelector('#comment-' + pk + ' > p').innerText
    document.querySelector('#update-comment-form textarea').value = comment
}

function pkField(form, pk) {
    document.querySelector('#' + form + ' input[name="comment-pk"]').value = pk
}
