let clickCounter = 0

document.addEventListener('DOMContentLoaded', () => {
    new Swiper('.teachers', {
        slidesPerView: 4,
        spaceBetween: 90,
        initialSlide: 0,
        // centeredSlides: true,
        loop: true,
        // loopedSlides: 1,

        autoplay: {
            delay: 2000,
            disableOnInteraction: false
        },
        speed: 800,

    })

    const profileContainer = document.querySelector('.profile-container')
    const texts = document.querySelectorAll('.teachers .teacher .text')
    const ice = document.querySelector('#ice')

    texts.forEach((el, idx) => {
        if (idx % 2 === 0) {
            el.classList.add('odd')
        }
    })

    profileContainer.style.marginTop = '60px'

    ice.addEventListener('click', () => {
        clickCounter++

        if (clickCounter === 16) {
            alert('Стопапупа')
        }
    })
})