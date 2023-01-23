let clickCounter = 0

document.addEventListener('DOMContentLoaded', () => {
    new Swiper('.teachers', {
        slidesPerView: 4,
        spaceBetween: 90,
        initialSlide: 0,
        loop: true,

        autoplay: {
            delay: 2000,
            disableOnInteraction: false
        },
        speed: 800,

        breakpoints: {
            700: {
                slidesPerView: 4,
            },

            500: {
                slidesPerView: 3,
            },

            100: {
                spaceBetween: 30,
                slidesPerView: 2,
            }
        }
    })

    new Swiper('.statistics', {
        slidesPerView: 3,
        slidesPerGroup: 3,
        initialSlide: 0,
        centeredSlides: true,
        loop: true,
        speed: 800,

        breakpoints: {
            700: {
                slidesPerView: 3,
            },

            400: {
                slidesPerView: 2,
                slidesPerGroup: 2,
            },

            100: {
                slidesPerView: 2,
                slidesPerGroup: 2,
            }
        },

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        }
    })

    const profileContainer = document.querySelector('.profile-container')
    const texts = document.querySelectorAll('.teachers .teacher .text')
    const ice = document.querySelector('#ice')
    const smoothLinks = document.querySelectorAll('a[href^="#"]')
    const copyrightLink = document.querySelector('#copyright')

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

    const text = document.createTextNode(new Date().getFullYear().toString())
    copyrightLink.appendChild(text)
})