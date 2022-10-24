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

    new Swiper('.statistics', {
        slidesPerView: 3,
        slidesPerGroup: 3,
        initialSlide: 0,
        centeredSlides: true,
        loop: true,
        speed: 800,
        // loopedSlides: 3,

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        }
    })

    const profileContainer = document.querySelector('.profile-container')
    const texts = document.querySelectorAll('.teachers .teacher .text')
    const ice = document.querySelector('#ice')
    const smoothLinks = document.querySelectorAll('a[href^="#"]')

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

     for (let smoothLink of smoothLinks) {
        smoothLink.addEventListener('click', function (e) {
            e.preventDefault();
            const id = smoothLink.getAttribute('href')

            document.querySelector(id).scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            })
        })
    }
})