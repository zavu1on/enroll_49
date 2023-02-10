document.addEventListener('DOMContentLoaded', async () => {

    const inputs = document.querySelectorAll('.input')
    const labels = document.querySelectorAll('label')
    let counter = 1

    for (let i = 0; i < inputs.length; i++) {
        const input = inputs[i]
        const label = labels[i]

        if (counter <= 2) {
            input.classList.add('primary')
            label.classList.add('primary')
        } else if (counter <= 4) {
            input.classList.add('secondary')
            label.classList.add('secondary')
        } else {
            counter = 1
        }

        counter++
    }

    const profileSelect = document.querySelector('#id_profile_class')
    const firstExamSelect = document.querySelector('#id_first_profile_exam')
    const secondExamSelect = document.querySelector('#id_second_profile_exam')

    firstExamSelect.querySelectorAll('option').forEach(opt => opt.remove())
    secondExamSelect.querySelectorAll('option').forEach(opt => opt.remove())

    const resp = await fetch('/api/profiles/')
    const data = await resp.json()

    profileSelect.addEventListener('change', event => {
        firstExamSelect.querySelectorAll('option').forEach(opt => opt.remove())
        secondExamSelect.querySelectorAll('option').forEach(opt => opt.remove())

        const exams = data.find(el => el.id.toString() === profileSelect.value).profile_exams

        const emptyOptionForFirstExamSelect = document.createElement('option')
        emptyOptionForFirstExamSelect.innerText = '---------'
        const firstOptionForFirstExamSelect = document.createElement('option')
        firstOptionForFirstExamSelect.innerText = exams[0].name
        firstOptionForFirstExamSelect.value = exams[0].id
        const secondOptionForFirstExamSelect = document.createElement('option')
        secondOptionForFirstExamSelect.innerText = exams[1].name
        secondOptionForFirstExamSelect.value = exams[1].id

        firstExamSelect.appendChild(emptyOptionForFirstExamSelect)
        firstExamSelect.appendChild(firstOptionForFirstExamSelect)
        firstExamSelect.appendChild(secondOptionForFirstExamSelect)

        const emptyOptionForSecondExamSelect = document.createElement('option')
        emptyOptionForSecondExamSelect.innerText = '---------'
        const firstOptionForSecondExamSelect = document.createElement('option')
        firstOptionForSecondExamSelect.innerText = exams[0].name
        firstOptionForSecondExamSelect.value = exams[0].id
        const secondOptionForSecondExamSelect = document.createElement('option')
        secondOptionForSecondExamSelect.innerText = exams[1].name
        secondOptionForSecondExamSelect.value = exams[1].id

        secondExamSelect.appendChild(emptyOptionForSecondExamSelect)
        secondExamSelect.appendChild(firstOptionForSecondExamSelect)
        secondExamSelect.appendChild(secondOptionForSecondExamSelect)
    })
})
