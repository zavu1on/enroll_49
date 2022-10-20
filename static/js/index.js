let clickCounter = 0

document.addEventListener('DOMContentLoaded', () => {
    const profileContainer = document.querySelector('.profile-container')
    const ice = document.querySelector('#ice')

    profileContainer.style.marginTop = '60px'

    ice.addEventListener('click', () => {
        clickCounter++

        if (clickCounter === 16) {
            alert('Стопапупа')
        }
    })
})