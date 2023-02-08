let clickCounter = 0

document.addEventListener('DOMContentLoaded', async () => {
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

    // statistic
    const resp = await fetch('/api/statistic/')
    const data = await resp.json()

    const statisticButtons = document.querySelectorAll('.profile-statistic')
    const enrollContent = document.querySelector('#enroll')
    const graduateContent = document.querySelector('#graduate')

    for (const btn of statisticButtons) {
        btn.addEventListener('click', event => {
            console.log(event.target.id, data)
            const active_statistic = data.find(s => s.id.toString() === event.target.id)

            if (active_statistic) {
                statisticButtons.forEach(btn => btn.classList.remove('active'))
                event.target.classList.add('active')

                enrollContent.innerHTML = `Всего поступило - ${active_statistic.number_of_received} человек(а)`
                graduateContent.innerHTML = `Всего выпустилось - ${active_statistic.number_of_graduates} ученик(ов)<br>Из них медалистов - ${active_statistic.number_of_medalists} ученик(ов)<br>В ВУЗ на бюджет поступили - ${active_statistic.number_of_state_employees} выпускник(ов)`
            }
        })
    }
})