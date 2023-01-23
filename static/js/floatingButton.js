let visible = false
let className = ''
let prevScroll = 0
const floatingButton = document.querySelector('#floatingButton')

document.addEventListener('scroll', () => {
    if (window.scrollY > prevScroll) {
        visible = true
        className = 'in'
    } else {
        visible = false
        className = 'out'
    }

    prevScroll = window.scrollY

    floatingButton.classList.remove('in', 'out', 'visible')

    floatingButton.classList.add(className)
    if (visible) {
        floatingButton.classList.add('visible')
    }
})
