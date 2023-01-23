document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.querySelector('#id_passport')
    const mask = new IMask(passwordInput, {
        mask: '0000-000000',
    })
})